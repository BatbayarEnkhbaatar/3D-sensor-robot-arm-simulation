import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from robotic_msgs.action import TesseraVueTasks
import open3d as o3d
import os
from pathlib import Path


def downsampling(input_file: Path, logger=None):
    """
    Loads, filters, and saves the point cloud.
    The output file is saved in the same directory as the input file.
    """
    input_path = Path(input_file)
    try:
        if logger:
            logger.info(f"Working on  point cloud from '{input_file}'...")

        # Read the point cloud file
        pcd = o3d.io.read_point_cloud(str(input_file))

        if pcd.is_empty():
            if logger:
                logger.error("Point cloud is empty. Aborting.")
            raise ValueError("Point cloud is empty.")

        if logger:
            logger.info(f"Loaded point cloud with {len(pcd.points)} points.")

        # Downsample the point cloud
        voxel_size = 0.00001
        if logger:
            logger.info(f"Downsampling point cloud with voxel size {voxel_size}...")
        voxel_down_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

        # Remove outliers
        cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        statistical_inliers = voxel_down_pcd.select_by_index(ind)

        # Create the output file path in the same directory as the input file
        output_file = input_path.parent / f"downsampled_{input_path.name}"
        # output_file = input_path.parent / f"downsampled_{input_file.name}"
        if output_file.exists():
            output_file.unlink()  # Remove the file if it already exists

        # Save the cleaned point cloud
        o3d.io.write_point_cloud(str(output_file), statistical_inliers)

        if logger:
            logger.info(f"Cleaned point cloud saved to '{output_file}'.")

    except Exception as e:
        if logger:
            logger.error(f"Error processing point cloud: {e}")
        raise

    return output_file
