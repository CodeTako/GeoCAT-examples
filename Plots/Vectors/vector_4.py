"""
vector_4
========

Plot U & V vectors globally, colored according to temperature

https://www.ncl.ucar.edu/Applications/Scripts/vector_4.ncl
"""

###############################################################################
# Import necessary packages
import xarray as xr
import numpy as np
from matplotlib import pyplot as plt
import cartopy
import cartopy.crs as ccrs

###############################################################################
# Read in data from netCDF file
file_in = xr.open_dataset('../../data/netcdf_files/83.nc').isel(time=0, lev=12)

###############################################################################
# Extract required variables from files
lat = file_in['lat']
lon = file_in['lon']

u = file_in['U']
v = file_in['V']
t = file_in['T']

###############################################################################
# Define a couple of utility functions
# to make plot look more like NCL style

# Helper function for defining NCL-like ax
def add_lat_lon_ticklabels(ax):
    """
    Nice latitude, longitude tick labels
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(zero_direction_label=False, dateline_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

def nclize_axis(ax):
    """
    Utility function to make plots look like NCL plots
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=1.5,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=5,
        width=0.75,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )

###############################################################################
# Make the plot

# Set up figure and axes
fig, ax = plt.subplots(figsize=(10,7))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.title('Vectors colored by a scalar map\n')
nclize_axis(ax)
add_lat_lon_ticklabels(ax)

# Set major and minor ticks
plt.xticks(range(-180, 181, 30))
plt.yticks(range(-90, 91, 30))

# Draw vector plot
# Notes
# 1. We plot every third vector in lat and every 5th in lon, which is not as nice as vcMinDistanceF in NCL
# 2. There is no matplotlib equivalent to "CurlyVector"
# Q = plt.quiver(lon[::5], lat[2::3], u.data[2::3, ::5], v.data[2::3, ::5], color=colors,
#                scale=(5/0.05), zorder=1, pivot="middle", width=0.001, headwidth=15)
Q = plt.quiver(lon[::5], lat[2::3], u.data[2::3, ::5], v.data[2::3, ::5], t.data[2::3, ::5], cmap='rainbow',
               scale=(5/0.05), zorder=1, pivot="mid", width=0.001, headwidth=15)

# Draw legend for vector plot
qk = ax.quiverkey(Q, 0.875, 0.8, 5, r'5 $m/s$', labelpos='N',
                  coordinates='figure', color='black', zorder=2)

cax = plt.axes((0.05, 0.025, 0.9, 0.05))
cbar  =fig.colorbar(Q, ax=ax, label='Temperature ($^{\circ}$K)', cax=cax,
                    orientation='horizontal', ticks=range(232,289,8))
# Turn on continent shading
feature = cartopy.feature.NaturalEarthFeature(name='coastline',
                                              category='physical',
                                              scale='50m',
                                              edgecolor='lightgray',
                                              facecolor='lightgray',
                                              zorder=0)
ax.add_feature(feature)

# Generate plot!
plt.show()