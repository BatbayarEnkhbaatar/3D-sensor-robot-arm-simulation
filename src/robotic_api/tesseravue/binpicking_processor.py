# binpicking_processor.py
"""
ObjectDetector3D: encapsulate YOLO + Open3D pipeline.
Handles both PNG/JPG _and_ raw grayscale frames, and rounds outputs.
"""

import os 
import math
import copy
import torch
import numpy as np
import cv2
import open3d as o3d
from ultralytics import YOLO


class ObjectDetector3D:
    def __init__(
        self,
        model_path: str,
        cad_model_path: str,
        device: str = 'cuda:0' if torch.cuda.is_available() else 'cpu',
        conf_threshold: float = 0.7,
        margin: int = 5
    ):  
        # print("Current working directory:", os.getcwd())
        # print("Absolute model path:", os.path.abspath(model_path))
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"YOLO model not found: {os.path.abspath(model_path)}")
        if not os.path.exists(cad_model_path):
            raise FileNotFoundError(f"CAD PCD not found: {cad_model_path}")

        self.model = YOLO(model_path).to(device)
        self.conf_threshold = conf_threshold
        self.margin = margin

        self.cad_pcd = o3d.io.read_point_cloud(cad_model_path)
        self.cad_center = np.mean(np.asarray(self.cad_pcd.points), axis=0)

    def load_image(self, img_bytes: bytes, xyz: np.ndarray | None = None) -> np.ndarray:
        """
        Try decoding PNG/JPG first; if that fails and xyz is provided,
        treat img_bytes as raw grayscale (one byte per pixel).
        """
        arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img is not None:
            return img

        if xyz is None:
            raise ValueError("Failed to decode image bytes (no shape info)")
        h, w, _ = xyz.shape
        gray = np.frombuffer(img_bytes, dtype=np.uint8)
        if gray.size != h*w:
            raise ValueError(f"Raw buffer size {gray.size} != h*w {h*w}")
        gray = gray.reshape((h, w))
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def run_yolo_segmentation(self, image: np.ndarray) -> list[dict]:
        h, w = image.shape[:2]
        results = self.model.predict(image, imgsz=(h, w), verbose=False)
        detections = []
        if results and results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            confs = results[0].boxes.conf.cpu().numpy()
            keep = confs > self.conf_threshold
            boxes = boxes[keep]
            masks = (results[0].masks.data.cpu().numpy()[keep]
                     if results[0].masks is not None else [None]*len(boxes))
            for (x1,y1,x2,y2), mask in zip(boxes, masks):
                x1 = int(max(0, x1 - self.margin))
                y1 = int(max(0, y1 - self.margin))
                x2 = int(min(w-1, x2 + self.margin))
                y2 = int(min(h-1, y2 + self.margin))
                mimg = (mask>0.5).astype(np.uint8)*255 if mask is not None else None
                detections.append({"bbox":[x1,y1,x2,y2], "mask":mimg})
        return detections

    def process(self, img_bytes: bytes, xyz: np.ndarray) -> dict:
        """
        img_bytes: PNG/JPG _or_ raw grayscale bytes
        xyz: (H,W,3) numpy array of points
        Returns:
          { "objects": [ {id, bounding_box, center_point, ICP:{…}} ] }
        with all floats rounded to 2 decimals.
        """
        image = self.load_image(img_bytes, xyz)
        h, w = image.shape[:2]
        detections = self.run_yolo_segmentation(image)
        results = []

        for i, det in enumerate(detections, start=1):
            x1,y1,x2,y2 = det["bbox"]
            mask = det["mask"]

            # 1) detection‐based centroid
            pts = xyz[y1:y2+1, x1:x2+1].reshape(-1,3)
            valid = (pts[:,0] != 10000)
            if not valid.any():
                continue
            center_arr = np.median(pts[valid], axis=0)

            # 2) segmentation pts (for ICP)
            seg_pts = []
            if mask is not None:
                for yy in range(y1, y2+1):
                    for xx in range(x1, x2+1):
                        if mask[yy,xx] and xyz[yy,xx,0] != 10000:
                            seg_pts.append(xyz[yy,xx])
            seg_pts = np.array(seg_pts)
            if seg_pts.size == 0:
                continue

            # 3) initial alignment
            T0 = np.eye(4)
            T0[:3,3] = center_arr - self.cad_center
            cad_t = copy.deepcopy(self.cad_pcd).transform(T0)

            # 4) down‐sample + normals
            seg_pcd   = o3d.geometry.PointCloud()
            seg_pcd.points = o3d.utility.Vector3dVector(seg_pts)
            vs = 0.005
            sd = seg_pcd.voxel_down_sample(vs)
            cd = cad_t.voxel_down_sample(vs)
            sd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=vs*2, max_nn=30))
            cd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=vs*2, max_nn=30))

            # 5) ICP
            icp = o3d.pipelines.registration.registration_icp(
                cd, sd, 0.02, np.eye(4),
                o3d.pipelines.registration.TransformationEstimationPointToPlane()
            )
            Tt = icp.transformation @ T0
            R = Tt[:3,:3]
            t = Tt[:3,3]

            # 6) euler angles
            yaw   = math.degrees(math.atan2(R[1,0], R[0,0]))
            pitch = math.degrees(math.atan2(-R[2,0],
                              math.sqrt(R[2,1]**2 + R[2,2]**2)))
            roll  = math.degrees(math.atan2(R[2,1], R[2,2]))

            # rounding
            c = [round(float(v),2) for v in center_arr]
            tr = [round(float(v),2) for v in t]
            ang = [round(roll,2), round(pitch,2), round(yaw,2)]

            results.append({
                "id": i,
                "bounding_box": {"top_left":[x1,y1], "bottom_right":[x2,y2]},
                "center_point": {"x":c[0], "y":c[1], "z":c[2]},
                "ICP": {
                    "fitness": round(icp.fitness,3),
                    "rmse":     round(icp.inlier_rmse,3),
                    "translation": {"x":tr[0], "y":tr[1], "z":tr[2]},
                    "euler_angles":{"roll":ang[0], "pitch":ang[1], "yaw":ang[2]}
                }
            })

        return {"objects": results}
