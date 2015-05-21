import probUCTdiscount

f = open('results3.txt', 'w')

for i in range(60):
	message = "\n\nRunning scenario 1000 times with R="+str(i/10.0)
	print message
	f.write(message)
	r, s = probUCTdiscount.iterateScenario(1000,0.9,i/10.0)
	f.write("\nAvg total reward: "+str(r))
	f.write("\t\tSuccess probability: "+str(s))

f.write("\n\nDone")

f.close()
