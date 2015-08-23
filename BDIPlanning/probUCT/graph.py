import matplotlib.pyplot as plt

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
	avgR.append(elements[1])
	avgS.append(elements[2])
	avgSR.append(elements[3])

	

plt.plot(rLevels,avgR,'g-')
plt.plot(rLevels,avgS,'r-')
plt.plot(rLevels,avgSR,'b-')
plt.axis([0,5,-100,100])
plt.ylabel('Total reward, Success rate')
plt.xlabel('R value')
plt.show()
