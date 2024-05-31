#include <iostream>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>

int main()
{
    pcl::PointCloud<pcl::PointXYZRGB> cloud;

    double radius= 3.0;
    int num_point=50;
    double angular_step_size = 2.0*M_PI/num_point;

    for(int i =0; i <num_point;i++){
    pcl::PointXYZRGB point;
    double angle = i *angular_step_size;
    point.x =radius * std::cos(angle);
    point.y =radius * std::sin(angle);
    point.z =1.0;
    
    point.r= 255*std::cos(angle);
    point.g= 255*std::sin(angle);
    point.b= 255*std::cos(angle +M_PI_2);
    
    cloud.push_back(point);
    }
    std::string path= "/home/baggi/ws_ros2/src/point_cloud_processing/data/cicrular.pcd";
    pcl::io::savePCDFileASCII(path, cloud);

    return 0;
}