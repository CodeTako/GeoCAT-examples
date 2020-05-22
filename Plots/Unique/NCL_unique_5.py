"""
NCL_unique_5.py
===============
This script illustrates the following concepts:
   - Plotting a bar chart
   - Creating a legend for a bar chart
   - Creating subplots in matplotlib

See following URLs to see the reproduced NCL plot & script:
    - Original NCL script: https://www.ncl.ucar.edu/Applications/Scripts/unique_5.ncl
    - Original NCL plot: https://www.ncl.ucar.edu/Applications/Images/unique_5_lg.png

"""

###############################################################################
# Import packages:
import numpy as np
import matplotlib.pyplot as plt
import random

from geocat.viz import util as gvutil

###############################################################################
# Generate labels:
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
          'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Generate random data:
obs = []
ccsm2_t42 = []
ccsm3_t42 = []
ccsm3_t85 = []

for i in range(12):
    obs.append(random.uniform(0.4, 1.2))
    ccsm2_t42.append(random.uniform(0.4, 1.2))
    ccsm3_t42.append(random.uniform(0.4, 1.2))
    ccsm3_t85.append(random.uniform(0.4, 1.2))

###############################################################################
# Create the custom color list.
color_list = ['red', 'grey', 'blue', 'green']

###############################################################################
# Specify some plot settings to use in both plots:

# Title settings
title = 'Nino3.4 Monthly Standard Deviation'
title_fontsize = 16

# Axis Settings
plot_y_max = 1.2

###############################################################################
# Plot bar chart with a legend

# Generate figure
plt.figure(2, figsize=(6, 5))
ax = plt.gca()

# Set width of each column
w = 0.15

# Create subplots for each category
sub = plt.subplot(111)
sub.bar(x+w, obs, width=0.15, color=color_list[0], edgecolor='black', align='center')
sub.bar((x+(2*w)), ccsm2_t42, width=0.15, color=color_list[1], edgecolor='black', align='center')
sub.bar(x+3*w, ccsm3_t42, width=0.15, color=color_list[2], edgecolor='black', align='center')
sub.bar(x+4*w, ccsm3_t85, width=0.15, color=color_list[3], edgecolor='black', align='center')

# Add label to each bar
for k, label in enumerate(labels):
    plt.text(x[k], -.05, label, rotation=0)

# Add the legend
plt.legend(['OBS', 'CCSM2 (T42)', 'CCSM3 (T42)', 'CCSM3 (T85)'], loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)

# Use geocat.viz.util convenience function to set axes limits & tick values
gvutil.set_axes_limits_and_ticks(ax, ylim=(0, plot_y_max), xticks=[], yticks=np.linspace(0.4, plot_y_max, 5))

# Use geocat.viz.util convenience function to add minor and major tick lines
gvutil.add_major_minor_ticks(ax, x_minor_per_major=0, y_minor_per_major=4, labelsize=12)

# Use geocat.viz.util convenience function to set titles and labels
gvutil.set_titles_and_labels(ax, maintitle=title, maintitlefontsize=title_fontsize, ylabel="(C"+u'\N{DEGREE SIGN}'+")")

# Show the plot
plt.tight_layout()
plt.show()
