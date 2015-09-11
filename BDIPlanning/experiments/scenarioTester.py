import sys
#import probUCTriskrollout as riskUCT
import finalprobUCT as riskUCT
import time

iters = 10000
gamma = 0.9
#R = 0#int(sys.argv[1])
exploreBias = 100
horizon = 100
rolloutcount = 10
state = riskUCT.s0

#f = open('probGraphs/results2plus.txt', 'w+')

def play(state, iters, gamma, R, exploreBias, horizon, rolloutcount):
	totalReward = 0
	success = 0
	
	while state.actions != []:
	
		decision = riskUCT.runUCT(state, iters, gamma, R, exploreBias, horizon, rolloutcount)
		#print "Doing action "+decision.action.name
		state = riskUCT.GetOutcome(decision.action)
		totalReward += riskUCT.GetReward(state, decision.action)
		#print "Outcome: "+state.name

		riskUCT.SetActions()
	
	if state.name == "s5":
		success = 1

	return success, totalReward


#generate r value based on number of robots left
def rule(n):
	if n == 3:
		return 1
	elif n==2:
		return 1
	elif n==1:
		return 1

def runAgent(agentName, inqueue, outqueue, wait):

	state = riskUCT.s0
	totalReward = 0

	nRobots = 3
	otherRobotSucceeded = False

	Rvalue = rule(nRobots)

	time.sleep(wait)

	print "Beginning "+agentName+" execution"
	while state.actions != [] and otherRobotSucceeded == False:
	
		#check to see if either another robot has faile dor succeded
		while not outqueue.empty():
			try:
				#print "Waiting on queue"
				message = outqueue.get_nowait()
				print agentName +" - received: "+ message
				if message == "f":		#a robot failed, change the R value
					nRobots -= 1
					Rvalue = rule(nRobots)	
					print "Agent "+agentName+ " R value now "+str(Rvalue)	
				elif message == "s":	#another robot succeeded, quit
					otherRobotSucceeded = True
			except:
				pass
	
		print agentName +" R = "+str(Rvalue)
		decision = riskUCT.runUCT(state, iters, gamma, Rvalue, exploreBias, horizon, rolloutcount)
		print agentName+ " is doing action "+decision.action.name
		state = riskUCT.GetOutcome(decision.action)
		totalReward += riskUCT.GetReward(state, decision.action)
		print agentName+" outcome: "+state.name

		riskUCT.SetActions()
		
		if state.name == "s5":		#we need to put it on twice t be read off by the (potentially) other 2 threads
			inqueue.put('s'+agentName+":"+str(totalReward))
	
		elif state.name == "s6":
			inqueue.put('f'+agentName+":0")
		


		
	
		



def iterate(iters, R):
	totalReward = 0.0
	successReward = 0.0
	successCount = 0.0

	for i in range(iters):
		s,t = play(state, iters, gamma, R, exploreBias, horizon, rolloutcount)
		successCount += s
		totalReward += t
		if s==1:
			successReward += t

	avgR = totalReward/iters
	avgS = successCount/iters * 100	#convert to percentage
	avgSR = successReward/successCount

	print avgR, avgS, avgSR
	fstring = str(R) + ","+str(avgR) + "," + str(avgS) + "," + str(avgSR) + ";"
	f.write(fstring)

def riskAdjust():
	R = 5.5
	for i in range(10):
		print "For R="+str(R)+":"
		iterate(1000, R)
		print "\n"
		R+=0.5

#print play(state, iters, gamma, 0, exploreBias, horizon, rolloutcount)
#riskAdjust()
