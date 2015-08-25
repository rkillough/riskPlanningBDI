import matplotlib.pyplot as plt
import matplotlib.pylab

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

	

plt.plot(rLevels,avgR,'g-', label='Average Reward')
plt.plot(rLevels,avgS,'r-', label='Success Rate (%)')
plt.plot(rLevels,avgSR,'b-', label='Average Reward when Successful')
plt.axis([0,10,-100,100])
plt.ylabel('Total reward, Success rate')
plt.xlabel('R value')
plt.legend()
plt.savefig('graph1.png')
plt.show()
