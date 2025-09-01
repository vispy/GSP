"""
Experiementation to measure the rendering time of the point cloud in matplotlib

- report written in a file
"""

import libs.point_cloud_lib as point_cloud_lib
import libs.point_cloud_bench as point_cloud_bench
import libs.download as download


# Experiment to handle intellisense in VSCode
import matplotlib.pyplot as plt
import numpy as np

from gsp.matplotlib import glm

# define __dirname__ to the directory of this script
import os
__dirname__ = os.path.dirname(os.path.abspath(__file__))

# Redirect stdout to a file
import sys
write_report_to_file = False  # Set to True to write the report to a file
if write_report_to_file:
    report_filename = os.path.join(__dirname__, '../output/lidar-benchmark-report.txt')
    print(f"Writing report to {report_filename}")
    sys.stdout = open(report_filename, 'w')


print("********** LIDAR Point Cloud Benchmark with Matplotlib *********")
# display matplotlib backend
print(f"Matplotlib backend: {plt.get_backend()}")

figsize = (6, 6)  # Size of the figure in inches
max_bench_delay_seconds = 20.0  # Maximum time to wait for the benchmark in seconds
wished_point_count = 200_000  # Number of points to keep after downsampling

###############################################################
# Load the LIDAR data
#

point_positions, point_colors = point_cloud_lib.load_npz_point_cloud(
    download.download_data("misc/lidar.npz")
)

print(f"Loaded LIDAR data with {len(point_positions)} points.")

point_cloud_lib.print_geometry_info(point_positions)

###############################################################################
# Crop geometry
#
point_positions, point_colors = point_cloud_lib.geometry_crop(
    point_positions=point_positions,
    point_colors=point_colors,
    x_min=-0.2,
    x_max=0.2,
    z_min=-0.2,
    z_max=0.2,
)

print(f"Cropped LIDAR data to {len(point_positions)} points.")

###############################################################################
# Downsample the point cloud
#

point_positions, point_colors = point_cloud_lib.downsample(
    point_positions=point_positions,
    point_colors=point_colors,
    wished_point_count=wished_point_count,
)

print(f"Downsampling - Keeping {len(point_positions)} points after downsampling.")


##################################################################################
# Perform 3d transform
#

# Compute the model-view-projection matrix
matrix_model = glm.xrotate(theta=20) @ glm.yrotate(theta=0)
matrix_view = glm.translate((0, 0, -3.5))
matrix_projection = glm.perspective(25, 1, 0.1, 100)
matrix_model_view_projection = matrix_projection @ matrix_view @ matrix_model

# convert to homogeneous coordinates and apply the MVP matrix
point_positions = (
    np.c_[point_positions, np.ones(len(point_positions))]
    @ matrix_model_view_projection.T
)

# Normalize point_positions for homogeneous coordinates
point_positions /= point_positions[:, 3].reshape(-1, 1)

###############################################################################
# Rendering on screen - good for debugging
#

measure_rendering_time = True  # Set to True to measure rendering time

if measure_rendering_time is False:
    # plt.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], s=1, rasterized=True)
    plt.scatter(point_positions[:, 0], point_positions[:, 1], color=point_colors, s=1, rasterized=True)

    plt.show(block=True)
    exit()


##########################################################################
# Benchmark rendering performance with monochrome points and manually defined projection
#

if True:
    print(f"\n********* Rendering the point cloud with Matplotlib... {len(point_positions)} points - monochrome - markers '.'")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], color=[1,0,0,1], marker='.', s=1, rasterized=False)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)

############################################################################
# Render the point cloud with colors  and manually defined projection
#
if True:
    print(f"\n********* Rendering the point cloud with Matplotlib... {len(point_positions)} points - colored - markers '.'")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], color=point_colors, marker='.', s=1, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)


###############################################################################
# benchmark rendering performance with monochrome markers and manually defined projection
#

if True:
    print(f"\n********* Rendering the point cloud with Matplotlib... {len(point_positions)} points - monochrome markers")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], marker='o', color=[1,0,0,1], s=2, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)

###############################################################################
# benchmark rendering performance with colored markers and manually defined projection
#
if True:
    print(f"\n********* Rendering the point cloud with Matplotlib... {len(point_positions)} points - colored markers")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot()
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], marker='o', color=point_colors, s=2, rasterized=True)
    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)

##########################################################################
# Benchmark rendering performance - with native 3D projection from matplotlib
if True:
    print(f"\n********* Benchmarking rendering performance with Matplotlib... {len(point_positions)} points with projection 3d from matplotlib")
    figure = plt.figure(figsize=figsize)
    axe = figure.add_subplot(projection='3d')
    axe.axis("off")  # Hide the axis
    axe.scatter(point_positions[:, 0], point_positions[:, 1], point_positions[:, 2], color=point_colors, s=1, rasterized=True)

    rendering_time = point_cloud_bench.display_benchmark_pure_matplotlib(figure=figure, log_enabled=True, max_bench_delay_seconds=max_bench_delay_seconds)
    print(f"Average rendering time: {rendering_time:.6f} seconds per rendering.")

    # Close the figure
    plt.close(figure)
