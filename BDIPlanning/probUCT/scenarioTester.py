import sys
import probUCTriskrollout as riskUCT

iters = 10000
gamma = 0.9
R = int(sys.argv[1])
exploreBias = 100
horizon = 100
rolloutcount = 5

state = riskUCT.s0




while state.actions != []:
	
	decision = riskUCT.runUCT(state, iters, gamma, R, exploreBias, horizon, rolloutcount)
	print "Doing action "+decision.action.name
	state = riskUCT.GetOutcome(decision.action)
	print "Outcome: "+state.name

	riskUCT.SetActions()
	
