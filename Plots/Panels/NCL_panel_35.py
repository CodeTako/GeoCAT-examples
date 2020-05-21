"""
NCL_panel_1.py
===============
This script illustrates the following concepts:
   - Attaching three filled contour plots along Y axes
   - Adding a common labelbar to attached plots
   - Adding a common title to attached plots
   - Generating dummy data using "generate_2d_array"
   - Drawing a custom labelbar
   - Drawing a custom title
   - Retrieving the bounding box of a plot

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: http://www.ncl.ucar.edu/Applications/Scripts/panel_35.ncl
    - Original NCL plot: http://www.ncl.ucar.edu/Applications/Images/panel_35_lg.png
"""

###############################################################################
# Import packages:
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
import geocat.viz.util as gvutil


###############################################################################
# Create figure and axes using gvutil
plt.figure()
fig, axs = plt.subplots(1, 3, figsize=(12,6),sharex='all', sharey='all', gridspec_kw={'wspace': 0})
gvutil.set_axes_limits_and_ticks(axs[0], xticks=np.arange(0,120,20), yticks=np.arange(0,120,20), xticklabels=np.arange(0,100,20), yticklabels=np.arange(0,100,20))
gvutil.add_major_minor_ticks(axs[0], x_minor_per_major=4, y_minor_per_major=4)
axs[0].tick_params(axis='both', which='both', top=True, left=True)

gvutil.set_axes_limits_and_ticks(axs[1], xticks=np.arange(0,120,20), yticks=np.arange(0,120,20), xticklabels=np.arange(0,100,20), yticklabels=np.arange(0,100,20))
gvutil.add_major_minor_ticks(axs[1], x_minor_per_major=4, y_minor_per_major=4)
axs[1].tick_params(axis='both', which='both', top=True, left=False, right=False)


gvutil.set_axes_limits_and_ticks(axs[2], xticks=np.arange(0,120,20), yticks=np.arange(0,120,20), xticklabels=np.arange(0,100,20), yticklabels=np.arange(0,100,20))
gvutil.add_major_minor_ticks(axs[2], x_minor_per_major=4, y_minor_per_major=4)
axs[2].tick_params(axis='both', which='both', top=True, left=False, right=True)

# Set title
fig.suptitle("Three dummy plots attached along Y axes")

# Create and plot dummy data
rand1 = np.random.uniform(low=-30, high=18, size=(100,100))
rand2 = np.random.uniform(low=-30, high=18, size=(100,100))
rand3 = np.random.uniform(low=-30, high=18, size=(100,100))

newcmap = gvcmaps.BlueYellowRed
axs[0].contourf(rand1, cmap = newcmap)
axs[1].contourf(rand2, cmap = newcmap)
p = axs[2].contourf(rand3, cmap = newcmap, levels=12)

cbar = fig.colorbar(p, orientation='horizontal', ax=axs, ticks=np.arange(-28,18,4), shrink=0.75)
plt.show()