"""
NCL_polyg_2.py
==============
Concepts illustrated:
  - Drawing a Lambert Conformal U.S. map color-coded by climate divisions
  - Color-coding climate divisions based on precipitation values
  - Drawing the climate divisions of the U.S.
  - Zooming in on a particular area on a Lambert Conformal map
  - Drawing a border around filled polygons
  - Masking the ocean in a map plot
  - Masking land in a map plot
  - Increasing the font size of text
  - Adding text to a plot
  - Drawing a custom labelbar on a map
  - Creating a red-yellow-blue color map

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/polyg_2.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/polyg_2_lg.png
"""

###############################################################################
# Import packages:
# ----------------
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
from geocat.viz import util as gvutil

import geocat.datafiles as gdf
import cartopy.io.shapereader as shpreader
import shapely.geometry as sgeom
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

###############################################################################
# Initialize color map and bounds for each color

colormap = colors.ListedColormap(['mediumpurple', 'mediumblue', 'royalblue', 'cornflowerblue', 'lightblue', 'teal', 'yellowgreen',
                                  'green', 'wheat', 'tan', 'gold', 'orange', 'red', 'firebrick'])

colorbounds = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100]

###############################################################################
# Define helper function to determine which color to fill the divisions based on precipitation data


def findDivColor(colorbounds, pdata):

    for x in range(len(colorbounds)):

        if pdata >= colorbounds[x]:
            continue
        else:
            # Index is 'x-1' because colorbounds is one item longer than colormap
            return colormap.colors[x-1]


###############################################################################
# Plot map

# Create plot figure
fig = plt.figure(figsize=(10, 10))

# Add a subplot for lambert conformal map
ax = fig.add_subplot(111, projection=ccrs.LambertConformal(), frameon=False, xbound=0.0, ybound=0.0)

# Set latitude and longitude extent of map
ax.set_extent([-119, -74, 18, 50], ccrs.Geodetic())

# Set shape name of map (which depicts the United States)
shapename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='110m', category='cultural', name=shapename)

# Set title and title fontsize of plot using gvutil function instead of matplotlib function call
gvutil.set_titles_and_labels(ax, maintitle="\nAverage Annual Precipiation \n Computed for the period 1899-1999 \n NCDC climate division data \n \n",
                             maintitlefontsize=18)

# Add outlines of each state within the United States
for state in shpreader.Reader(states_shp).geometries():

    facecolor = 'white'
    edgecolor = 'black'

    ax.add_geometries([state], ccrs.PlateCarree(), facecolor=facecolor, edgecolor=edgecolor)

# Open climate division datafile and add to xarray
ds = xr.open_dataset(gdf.get("netcdf_files/climdiv_prcp_1899-1999.nc"), decode_times=False)

# For each variable (climate division) in data set, create outline on map and fill with random color
for varname, da in ds.data_vars.items():

    try:
        # Get precipitation data for each climate division
        precipitationdata = sum(da.values)/100

        # Get borders of each climate division
        lat = da.lat
        lon = da.lon

        # Get color of climate division
        color = findDivColor(colorbounds, precipitationdata)

        # Use "shapely geometry" module to create division outlines from lat/lon coordinates
        track = sgeom.LineString(zip(lon, lat))

        # Add division outlines to map
        im = ax.add_geometries([track], ccrs.PlateCarree(), facecolor=color, edgecolor='k', linewidths=.5)

    except Exception as E:
        print(E)
        continue

###############################################################################
# Plot colorbar

# Map colors to bounds
norm = colors.BoundaryNorm(colorbounds, colormap.N)

# Adjust size of colorbar with "inset_axes" function
axins1 = inset_axes(ax,
                    width="75%",  # width = 50% of parent_bbox width
                    height="3%",  # height : 5%
                    loc='lower center'
                    )

# Add colorbar to plot
cb = fig.colorbar(cm.ScalarMappable(cmap=colormap, norm=norm), cax=axins1, boundaries=colorbounds,
                  ticks=colorbounds, spacing='uniform', orientation='horizontal', label='inches')

plt.show()
