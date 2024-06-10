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
    pcl::PointCloud<PointT>::Ptr passthrough_cloud(new pcl::PointCloud<PointT>);
    pcl::PCDReader cloud_reader;

    // Reading the point cloud data
    std::string path = "/home/baggi/ws_ros2/src/point_cloud_processing/data/";
    std::string cloud_name = "data.pcd";
    cloud_reader.read(path + cloud_name, *cloud);


    // Pass-through filter along with x axis
    pcl::PassThrough<PointT> passing_x;
    passing_x.setInputCloud(cloud);
    passing_x.setFilterFieldName("x");
    passing_x.setFilterLimits(-1.5, 1.5);
    passing_x.setNegative(true);
    passing_x.filter(*passthrough_cloud);

    // Pass-through filter along with y axis
    pcl::PassThrough<PointT> passing_y;
    passing_y.setInputCloud(cloud); 
    passing_y.setFilterFieldName("y");
    passing_y.setFilterLimits(-1.5, 1.5);
    passing_y.setNegative(true);
    passing_y.filter(*passthrough_cloud); 

    // Pass-through filter along with z axis
    pcl::PassThrough<PointT> passing_z;
    passing_z.setInputCloud(cloud); 
    passing_z.setFilterFieldName("z");
    passing_z.setFilterLimits(-1.5, 1.5);
    passing_z.setNegative(true);
    passing_z.filter(*passthrough_cloud); 


    // Cloud writing

    cloud_saver("pass_through.pcd", path, passthrough_cloud);


    return 0;
}
