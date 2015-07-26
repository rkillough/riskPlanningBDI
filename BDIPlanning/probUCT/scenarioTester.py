import probUCTv5 as riskUCT

iters = 10000
gamma = 0.9
R = 3
exploreBias = 100
horizon = 100

state = riskUCT.s0




while state.actions != []:
	
	decision = riskUCT.runUCT(state, iters, gamma, R, exploreBias, horizon)
	print "Doing action "+decision.action.name
	state = riskUCT.GetOutcome(decision.action)
	print "Outcome: "+state.name

	riskUCT.SetActions()
	
