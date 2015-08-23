import sys
import probUCTriskrollout as riskUCT

iters = 10000
gamma = 0.9
#R = 0#int(sys.argv[1])
exploreBias = 100
horizon = 100
rolloutcount = 5
state = riskUCT.s0

f = open('results.txt', 'w')

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
	R = 0
	for i in range(11):
		print "For R="+str(R)+":"
		iterate(10, R)
		print "\n"
		R+=0.5

riskAdjust()
