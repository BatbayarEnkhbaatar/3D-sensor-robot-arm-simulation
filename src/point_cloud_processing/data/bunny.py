import open3d as o3d
import numpy as np


bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)
mesh.compute_vertex_normals()

o3d.visualization.draw_geometries([mesh])
pcd = mesh.sample_points_uniformly(number_of_points=5000)
print(pcd)
o3d.io.write_triangle_mesh("bunny.stl", mesh)
o3d.visualization.draw_geometries([pcd])
