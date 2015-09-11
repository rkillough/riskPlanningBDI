#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 4
menMeans = (57,67,93,81)
menStd =   (2, 3, 4, 1)

ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, menMeans, width, color='0.9')

womenMeans = (90,55,9.7,52.77)
womenStd =   (3, 5, 2, 3)
rects2 = ax.bar(ind+width, womenMeans, width, color='0.4')


ax2 = plt.twinx()
# add some text for labels, title and axes ticks
ax.set_ylabel('Total Reward')
#ax.set_title('R values')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Static 0', 'Static 2', 'Static 4.5', 'Variable') )

ax2.axis([0,4,0,100])
ax2.set_ylabel("Success Rate (%)")

ax.legend( (rects1[0], rects2[0]), ('Success rate (%)', 'Avg reward when successful'), loc=3, prop={'size':10} )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)

plt.savefig('bar.png')
plt.show()
