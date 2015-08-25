import matplotlib.pyplot as plt

f = open('results.txt', 'r')
string = f.read()

plt.plot([0,1],[-50,-100],'g-')
plt.plot([0,1],[50,100],'r-')
plt.plot([0,1],[55,-10],'b-')
plt.axis([0,5,-100,100])
plt.ylabel('Total reward, Success rate')
plt.xlabel('R value')
plt.show()
