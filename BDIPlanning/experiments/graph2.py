import matplotlib.pyplot as plt
import matplotlib.pylab as pylab


f = open('results.txt', 'r')
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
	avgS.append(elements[1])
	print elements[1]
	avgSR.append(elements[2])

	
ax = plt.gca()
ax2 = plt.twinx()

x = [1,2,3,4]
plt.xticks(x,rLevels)
y = [0,100]

ax2.plot(x,avgS,'r-', label='Success Rate (%)')
ax.plot(x,avgSR,'b-', label='Avg Reward when Successful')
#ax.axis([0,10,-1000,1000])
ax.axis([1,4,0,100])

ax2.axis([1,4,0,100])

ax.set_ylabel('Total reward')
ax2.set_ylabel('Success rate (%)')
ax.set_xlabel('R values')

ax.legend()
ax.legend(loc=2)
ax2.legend(loc=4)
#plt.legend()
plt.savefig('graph.png')
plt.show()
