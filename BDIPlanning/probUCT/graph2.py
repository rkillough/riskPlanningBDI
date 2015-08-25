import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


f = open('results3.txt', 'r')
raw = f.read()
#print string

rSets = raw.split(';')[:-1]
rLevels = []
avgR = []
avgS = []
avgSR =[]
for x in rSets:
	print x
	elements = x.split(',')
	rLevels.append(elements[0])
	avgR.append(elements[1])
	avgS.append(elements[2])
	avgSR.append(elements[3])

	
ax = plt.gca()
ax2 = plt.twinx()

ax.plot(rLevels,avgR,'g-', label='Avg Reward')
ax2.plot(rLevels,avgS,'r-', label='Success Rate (%)')
ax.plot(rLevels,avgSR,'b-', label='Avg Reward when Successful')
ax.axis([0,10,-100,100])
ax2.axis([0,10,0,100])


ax.set_ylabel('Total reward')
ax2.set_ylabel('Success rate (%)')
ax.set_xlabel('R value')

ax.legend()
ax.legend(loc=2)
ax2.legend(loc=1)
#plt.legend()
plt.savefig('graph1.png')
plt.show()
