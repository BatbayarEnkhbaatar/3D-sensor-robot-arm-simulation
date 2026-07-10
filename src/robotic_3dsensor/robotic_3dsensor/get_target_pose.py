import rclpy
from rclpy.node import Node
from robotic_msgs.action import TesseraVueTasks
from rclpy.action import ActionServer
import open3d as o3d
from std_msgs.msg import Float64MultiArray
import numpy as np
import os
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
import shutil
import array
class GetTargetObjectPublisher(Node):

    def __init__(self):
        super().__init__('getTarget_object_publisher')
        self.publisher_ = self.create_publisher(Float64MultiArray, 'detection_results', 10)

        self.timer = self.create_timer(1, self.timer_callback)
        
        self._action_server = ActionServer(
            self,
            TesseraVueTasks,
            'TesseraVueTasks',
            self.execute_callback
        )
        package_name = 'robotic_3dsensor'
        self.get_logger().info("Target Coordinates Action Server get started ...")
        self.package_share_directory = get_package_share_directory(package_name)
        self.local_directory = os.path.join(self.package_share_directory, 'data')  
        self.pcd_directory = os.path.join(self.package_share_directory, 'data')
        #
    def timer_callback(self):
        msg = Float64MultiArray()
        # msg.data = [1.1,2.2,3.2]
        # self.publisher_.publish(msg)
        # self.get_logger().info('lISTENNING!!')
        # self.i += [1,1,1]
    
    
    def seperate_inlier_outlier(self, cloud, ind):
        """Visualize inliers and outliers, and return inlier cloud."""
        # Separate inliers and outliers
        inlier_cloud = cloud.select_by_index(ind)
        outlier_cloud = cloud.select_by_index(ind, invert=True)

        self.get_logger().info("Showing outliers (red) and inliers (gray): ")
        outlier_cloud.paint_uniform_color([1, 0, 0]) 
        inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8]) 
        return inlier_cloud
    
    def execute_callback(self, goal_handle):
        result = TesseraVueTasks.Result()
        result_coordinates = Float64MultiArray()

        goal = goal_handle.request
        if not goal.lastshots or len(goal.lastshots) < 1:
            self.get_logger().error("No PCD file provided in goal request.")
            result.success = False
            return result

        pcd_file = goal.lastshots[0]
        self.get_logger().info(f"Processing PCD File: {pcd_file}")
        
        try:
            # Load the PCD file
            pcd = o3d.io.read_point_cloud(pcd_file)
            if not pcd.has_points():
                self.get_logger().error("PCD file contains no points.")
                result.success = False
                return result

            # Apply voxel down-sampling
            voxel_size = 0.00001
            voxel_down_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)
            
            # Save the downsampled point cloud in the same directory
            downsampled_file = os.path.join(os.path.dirname(pcd_file), "downsampled.pcd")
            o3d.io.write_point_cloud(downsampled_file, voxel_down_pcd)
            self.get_logger().info(f"Saved downsampled PCD to {downsampled_file}")

            # Apply statistical outlier removal
            cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=5, std_ratio=2.0)
            inlier_cloud = voxel_down_pcd.select_by_index(ind)

            # Save the cleaned point cloud
            output_file = pcd_file  # Overwriting the same file
            if os.path.exists(output_file):
                self.get_logger().info(f"Removing existing file: {output_file}")
                os.remove(output_file)
            

   
            o3d.io.write_point_cloud(output_file, inlier_cloud)
            
            # axis = o3d.geometry.create_mesh_coordinate_frame(size=5.0, origin=array([0., 0., 0.]))
            # Open visualization
            
            # mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=6, origin=[0, 0, 0])
            if os.environ.get("DISPLAY", "") != "":
                vis = o3d.visualization.VisualizerWithEditing()
                vis.create_window("PCD Viewer")

                # Add point cloud
                
                # vis.add_geometry()
                vis.add_geometry(inlier_cloud)

                
                vis.run()  # Block execution for user selection
                vis.destroy_window()

            picked_indices = vis.get_picked_points()
            if not picked_indices:
                self.get_logger().error("No points selected by the user.")
                result.success = False
                return result

            selected_points = np.asarray(inlier_cloud.points)[picked_indices]
            self.get_logger().info("Selected Points (X, Y, Z):")
            for i, point in enumerate(selected_points):
                self.get_logger().info(f"Point {i + 1}: {point}")

            # Choose target point (e.g., first selected point)
            target_point = selected_points[0]
            self.get_logger().info(f"Target Point: {target_point}")
            result_coordinates.data = target_point.tolist()
            
            # Publish result
            self.publisher_.publish(result_coordinates)
            self.get_logger().info(f"Published target coordinates: {result_coordinates.data} on TOPIC detection_results")
            
            # Set result success
            result.success = True
            goal_handle.succeed()
            return result
        
        except Exception as e:
            self.get_logger().error(f"Failed to process PCD file: {str(e)}")
            result.success = False
            return result

    

def main(args=None):
    rclpy.init(args=args)

    target_cooridantes_publisher = GetTargetObjectPublisher()

    rclpy.spin(target_cooridantes_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    target_cooridantes_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()