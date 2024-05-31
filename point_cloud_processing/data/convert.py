import open3d as o3d
import numpy as np
import trimesh

pcd_file = "/home/baggi/ws_ros2/src/point_cloud_processing/data/data.pcd"
stl_file = "output.stl"
pcd = o3d.io.read_point_cloud(pcd_file)
pcd.estimate_normals()
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 1.5 * avg_dist   

mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
           pcd,
           o3d.utility.DoubleVector([radius, radius * 2]))

# create the triangular mesh with the vertices and faces from open3d
tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
                          vertex_normals=np.asarray(mesh.vertex_normals))

trimesh.convex.is_convex(tri_mesh)


# bunny = o3d.data.BunnyMesh()
# mesh = o3d.io.read_triangle_mesh(pcd_file)
# mesh.compute_vertex_normals()
# print("Visualizing the mesh file")
# o3d.visualization.draw_geometries([mesh])
# pcd = mesh.sample_points_uniformly(number_of_points=50000)
# o3d.visualization.draw_geometries([pcd])
# print(pcd)
# o3d.io.write_triangle_mesh("terraVueObject.stl", mesh)
# o3d.visualization.draw_geometries([pcd])
