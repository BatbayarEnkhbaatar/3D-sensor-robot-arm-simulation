#include <iostream>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/passthrough.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/extract_indices.h>

typedef pcl::PointXYZ PointT;

void cloud_saver (const std::string & file_name,std::string& path, pcl::PointCloud<PointT>::Ptr cloud_arg){
    pcl::PCDWriter cloud_writer;
    cloud_writer.write<PointT> (path+std::string(file_name), *cloud_arg);
}

int main()
{
    pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);
    pcl::PointCloud<PointT>::Ptr voxel_cloud(new pcl::PointCloud<PointT>);
    pcl::PointCloud<PointT>::Ptr passthrough_cloud(new pcl::PointCloud<PointT>);
    pcl::PCDReader cloud_reader;

    // Reading the point cloud data
    std::string path = "/home/baggi/ws_ros2/src/point_cloud_processing/data/";
    std::string cloud_name = "data.pcd";
    cloud_reader.read(path + cloud_name, *cloud);

    // Voxel filter
    pcl::VoxelGrid<PointT> voxel_filter;
    voxel_filter.setInputCloud(cloud);
    voxel_filter.setLeafSize(1.1, 1.1, 1.1);
    voxel_filter.filter(*voxel_cloud);

    // Pass-through filter along with x axis
    pcl::PassThrough<PointT> passing_x;
    passing_x.setInputCloud(cloud);
    passing_x.setFilterFieldName("x");
    passing_x.setFilterLimits(-3.5, 3.5);
    passing_x.setNegative(true);
    passing_x.filter(*passthrough_cloud);

    // Pass-through filter along with y axis
    pcl::PassThrough<PointT> passing_y;
    passing_y.setInputCloud(cloud); 
    passing_y.setFilterFieldName("y");
    passing_y.setFilterLimits(-3.5, 3.5);
    passing_y.setNegative(true);
    passing_y.filter(*passthrough_cloud); 

    // Plane Segmentation

    pcl::PointIndices::Ptr inliers(new pcl::PointIndices);
    pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);
    pcl::PointCloud<PointT>::Ptr plane_segmented_cloud(new pcl::PointCloud<PointT>);
    pcl::SACSegmentation<PointT> plane_segmentor;
    pcl::ExtractIndices<PointT> indices_extractor;

    plane_segmentor.setInputCloud(passthrough_cloud); 
    plane_segmentor.setModelType(pcl::SACMODEL_PLANE);
    plane_segmentor.setMethodType(pcl::SAC_RANSAC);
    plane_segmentor.setDistanceThreshold(0.02); 
    plane_segmentor.segment(*inliers, *coefficients);
    indices_extractor.setInputCloud(passthrough_cloud); 
    indices_extractor.setIndices(inliers);
    indices_extractor.setNegative(false);
    indices_extractor.filter(*plane_segmented_cloud);
    // Cloud writing
    cloud_saver("voxel_filtered.pcd", path, voxel_cloud);
    cloud_saver("pass_through.pcd", path, passthrough_cloud);
    cloud_saver("plane_segmented.pcd", path, plane_segmented_cloud);
    return 0;
}
