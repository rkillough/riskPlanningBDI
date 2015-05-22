import probUCTdomain

f = open('results/results5.csv', 'w')

for i in range(11):
	message = "\n\nRunning scenario 1000 times with R="+str(i/2.0)
	print message
	#f.write(message)
	r, s, sr = probUCTdomain.iterateScenario(100,0.9,i/2.0)
	f.write(str(r))
	f.write(","+str(s*100))
	f.write(","+str(sr)+"\n")

print "Done"

f.close()
