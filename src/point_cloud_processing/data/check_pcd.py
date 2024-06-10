import open3d as o3d
import numpy as np
# Load point cloud data from PCD file
pcd = o3d.io.read_point_cloud("data.pcd")
print(pcd)
down_pcd = pcd.uniform_down_sample(every_k_points = 100)
print(down_pcd)
print(np.asanyarray(len(down_pcd.points)))
o3d.visualization.draw_geometries([down_pcd])


# o3d.visualization.draw_geometries([pcd])