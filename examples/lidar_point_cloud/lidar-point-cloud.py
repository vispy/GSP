"""
Display a point cloud of a terrain

- inspired from datoviz library - https://datoviz.org/gallery/showcase/lidar/
"""

import gsp

# Experiment to handle intellisense in VSCode
from gsp.matplotlib import core, visual, glm
import matplotlib.pyplot as plt
import numpy as np

# Display matplotlib backend
print(f"Matplotlib backend: {plt.get_backend()}")


import libs.point_cloud_lib as point_cloud_lib
import libs.point_cloud_display as point_cloud_display
import libs.download as download

# Set up gsp.logging
import logging
gsp.log.setLevel(logging.INFO)

###############################################################################
# Load the LIDAR data
#
point_positions, point_colors = point_cloud_lib.load_npz_point_cloud(
    download.download_data("misc/lidar.npz")
)
print(f"Loaded LIDAR data with {len(point_positions)} points.")
gsp.log.warning(f"Loaded LIDAR data with {len(point_positions)} points.")

###############################################################################
# Crop geometry
#
point_positions, point_colors = point_cloud_lib.geometry_crop(
    point_positions=point_positions,
    point_colors=point_colors,
    x_min=-0.1,
    x_max=0.1,
    z_min=-0.1,
    z_max=0.1,
)

print(f"Loaded LIDAR data with {len(point_positions)} points.")

###############################################################################
# Downsample the point cloud
#
point_positions, point_colors = point_cloud_lib.downsample(
    point_positions=point_positions,
    point_colors=point_colors,
    # wished_point_count=5_000_000
    # wished_point_count=400_000,
    wished_point_count=200_000,
    # wished_point_count=10_000,
)

print(f"Downsampling - Keeping {len(point_positions)} points after downsampling.")

###############################################################################
# Display geometry information
#
point_cloud_lib.print_geometry_info(point_positions)

###############################################################################
# Display the point cloud
#
point_cloud_display.display_gsp(point_positions, point_colors)
# point_cloud_display.display_gsp_dual_resolution(point_positions, point_colors)
