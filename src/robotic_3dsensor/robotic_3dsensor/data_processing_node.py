import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from robotic_msgs.action import TesseraVueTasks
import open3d as o3d
import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
import shutil

class PointCloudFilterNode(Node):
    def __init__(self):
        #
        super().__init__("point_cloud_filter")
        self.get_logger().info("Point Cloud Filter Node has started.")
        package_name = 'robotic_object_detection'
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data')  
        self.pcd_directory = os.path.join(self.package_share_directory, 'data')
        #
        input_file =  self.get_latest_pcd_file(self.pcd_directory)
        if not input_file[0]:
            self.get_logger().error("No PCD file found in the directory!!!")
        if not input_file[1]:
            self.get_logger().error("No BMP file found in the directory!!!")    

        self.get_logger().info(f"Processing the latest PCD file: {input_file[0]}")
        self.get_logger().info(f"Processing the latest 2D image: {input_file[1]}")

        # 
        output_file_pcd = "/cleaned_data.pcd"
        output_file_bmp = self.local_directory + "/" + "cleaned_data.bmp"

        self.get_logger().info(f"{input_file[0]} is being processed ...")

        self.timer = self.create_timer(3.0, lambda: self.process_point_cloud(input_file=input_file[0], output_file=self.local_directory + output_file_pcd))

        os.rename(input_file[1], "cleaned_data.bmp")

    def get_latest_pcd_file(self, directory: Path):
        try:
            directory = Path(directory)  # Ensure directory is a Path object
            
            # Filter out 'cleaned_data.pcd' and get all other '.pcd' files
            pcd_files = [
                file for file in directory.glob("*.pcd")
                if file.name != "cleaned_data.pcd"
            ]
            # Filter out 'cleaned_data.bmp' and get all other '.bmp' files
            bmp_files = [
                file for file in directory.glob("*.bmp")
                if file.name != "cleaned_data.bmp"
            ]
            if not pcd_files:
                return None
            latest_pcd_file = max(pcd_files, key=os.path.getmtime)

            if not bmp_files:
                return None
            latest_bmp_file = max(bmp_files, key=os.path.getmtime)
            return latest_pcd_file, latest_bmp_file
        except Exception as e:
            print(f"Error while fetching latest files: {e}")
            return None
        
    def process_point_cloud(self, input_file: Path, output_file: str):
        try:
            #
            self.get_logger().info(f"Loading point cloud from '{input_file}'...")
            pcd = o3d.io.read_point_cloud(str(input_file))
            if pcd.is_empty():
                self.get_logger().warn("Point cloud is empty!")
                # return
            self.get_logger().info(f"Loaded point cloud with {len(pcd.points)} points.")
            # Downsample point cloud
            voxel_size = 0.00001
            self.get_logger().info(f"Downsampling point cloud with voxel size {voxel_size}...")
            voxel_down_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
            self.get_logger().info(f"Downsampled point cloud has {len(voxel_down_pcd.points)} points.")

            self.get_logger().info("Applying statistical outlier removal...")
            cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=5, std_ratio=2.0)
            # Separate inliers and outliers
            inlier_cloud = self.seperate_inlier_outlier(voxel_down_pcd, ind)
            if os.path.exists(output_file):
                self.get_logger().info(f"Removing existing file: {output_file}")
                os.remove(output_file)
            # Save the cleaned point cloud
            self.get_logger().info(f"Saving cleaned point cloud to '{output_file}'...")
            o3d.io.write_point_cloud(output_file, inlier_cloud)
            self.get_logger().info("Cleaned point cloud saved successfully.")

        except Exception as e:
            self.get_logger().error(f"Error processing point cloud: {e}")

    def seperate_inlier_outlier(self, cloud, ind):
        """Visualize inliers and outliers, and return inlier cloud."""
        # Separate inliers and outliers
        inlier_cloud = cloud.select_by_index(ind)
        outlier_cloud = cloud.select_by_index(ind, invert=True)

        self.get_logger().info("Showing outliers (red) and inliers (gray): ")
        outlier_cloud.paint_uniform_color([1, 0, 0]) 
        inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8]) 
        return inlier_cloud

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
