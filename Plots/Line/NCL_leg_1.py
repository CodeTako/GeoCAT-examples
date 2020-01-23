"""
leg_1.py
===============
Plots/Lines/Legends
"""

###############################################################################
# 
# import modules
import numpy as np
import xarray as xr

import matplotlib.pyplot as plt


###############################################################################
# 
# open data file and extract variables
ds = xr.open_dataset('../../data/netcdf_files/uv300.nc')
uz = ds.U.mean(dim=['lon','time'])
vz = ds.V.mean(dim=['lon','time'])

###############################################################################
# 
# create plot
plt.figure(figsize=(5,5))
plt.plot(vz.lat, vz.values, '--', c='gray', label='V')
plt.plot(uz.lat, uz.values, c='gray', label='U')

plt.ylim([-10,40])
plt.xlim([-90,90])

xticks = [-90, -60, -30, 0, 30, 60, 90]
xlabels = ['90S', '60S', '30S', '0', '30N', '60N', '90N']
plt.xticks(xticks, xlabels)
plt.minorticks_on()
plt.tick_params(which='both',right=True, top=True)


plt.legend(loc='upper left', frameon=False, prop={'weight':'bold'})
plt.show();

