"""
NCL_xy_18.py
============
Concepts illustrated:

- Filling the area between two curves in an XY plot
- Labeling the bottom X axis with years
- Drawing a main title on three separate lines
- Calculating a weighted average
- Changing the size/shape of an XY plot using viewport resources
- Manually creating a legend
- Overlaying XY plots on each other
- Maximizing plots after they've been created

See the [original NCL example](https://www.ncl.ucar.edu/Applications/Scripts/xy_18.ncl)
"""

###############################################################################
# Basic imports
import numpy as np
import xarray as xr
from matplotlib import pyplot as plt
import matplotlib.ticker as tic

###############################################################################
# Open files and read in monthly data

def assume_noleap_calendar(ds):
    ds.time.attrs['calendar'] = 'noleap'
    return xr.decode_cf(ds)

nfiles = ["../../data/netcdf_files/TREFHT.B06.66.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.67.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.68.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.69.atm.1890-1999ANN.nc"]
nds = xr.open_mfdataset(nfiles, concat_dim='case', combine='nested',
                        preprocess=assume_noleap_calendar,
                        use_cftime=True, decode_times=False)

vfiles = ["../../data/netcdf_files/TREFHT.B06.61.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.59.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.60.atm.1890-1999ANN.nc",
          "../../data/netcdf_files/TREFHT.B06.57.atm.1890-1999ANN.nc"]
vds = xr.open_mfdataset(vfiles, concat_dim='case', combine='nested',
                        preprocess=assume_noleap_calendar,
                        use_cftime=True, decode_times=False)

gds = xr.open_dataset("../../data/netcdf_files/gw.nc")
gds = gds.expand_dims(dim={'lon': nds.lon})

###############################################################################
# Some parameters
nyrs = len(nds["time"])
nlon = len(nds["lon"])
nlat = len(nds["lat"])
time =

###############################################################################
# OBS

obs = np.loadtxt("../../data/ascii_files/jones_glob_ann_2002.asc", dtype=float)

###############################################################################
# NCL-based Weighted Mean Function

def horizontal_weighted_mean(var, wgts):
    return (var * wgts).sum(dim=['lat', 'lon']) / wgts.sum(dim=['lat', 'lon'])

###############################################################################
# NATURAL

gavn = horizontal_weighted_mean(nds["TREFHT"], gds["gw"])
gavan = gavn - gavn.isel(time=slice(0,30)).mean(dim='time')

###############################################################################
# ALL

gavv = horizontal_weighted_mean(vds["TREFHT"], gds["gw"])
gavav = gavv - gavv.isel(time=slice(0,30)).mean(dim='time')

###############################################################################
# CALCULATE ENSEMBLE MIN & MAX

gavan_min = gavan.min(dim='case')
gavan_max = gavan.max(dim='case')
gavan_avg = gavan.mean(dim='case')

gavav_min = gavav.min(dim='case')
gavav_max = gavav.max(dim='case')
gavav_avg = gavav.mean(dim='case')

obs_avg = obs[34:144] - np.mean(obs[34:64])

###############################################################################
# Create plot

fig, ax = plt.subplots(figsize=(10.5, 6))

ax.tick_params(labelsize="small")
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.tick_params(axis="both", labelsize=20)
ax.tick_params("both", length=8, width=1.50, which="major", bottom=True, top=True, left=True, right=True)
ax.tick_params("both", length=5, width=0.75, which="minor", bottom=True, top=True, left=True, right=True)

time = gavan.time.values

ax.set_title('Parallel Climate Model Ensembles', fontsize=24, pad=60.0)
ax.text(0.5, 1.125, 'Global Temperature Anomalies', fontsize=18, ha='center', va='center', transform=ax.transAxes)
ax.text(0.5, 1.06, 'from 1890-1919 average', fontsize=14, ha='center', va='center', transform=ax.transAxes)
ax.set_ylabel('$^\circ$C', fontsize=24)
ax.fill_between(time, gavan_min, gavan_max, color='lightblue')
ax.fill_between(time, gavav_min, gavav_max, color='lightpink')

xmin = cftime.DatetimeNoLeap(1890, 7, 16, hour=22)
xmax = cftime.DatetimeNoLeap(2000, 7, 16, hour=22)
ax.set_xlim(xmin=xmin, xmax=xmax)
ax.set_ylim(ymin=-0.4, ymax=1)
#ax.set_xticks([cftime.DatetimeNoLeap(i, 7, 16, hour=22) for i in range(1900, 2001, 20)])
ax.set_yticks(np.arange(-0.3, 1, step=0.3))

p_n, = ax.plot(time, gavan_avg, color='blue', label='Natural')
p_v, = ax.plot(time, gavav_avg, color='red', label='Anthropogenic + Natural')
p_o, = ax.plot(time, obs_avg, color='black', label='Observations')

handles, labels = ax.get_legend_handles_labels()

ax.legend(handles[::-1], labels[::-1], loc='upper left', frameon=False, fontsize=18)

plt.show()
