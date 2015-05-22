'''
Generates a random domain as per the specified parameters

Each state comprises a name (just a number 0...n) and a list of actions
These are the actions available to be taken at that state

Each Action contains a name, a list of states (outcomes of taking this action), a list of probabilities and a list of rewards
The probabilities correspond the the chance of arriving in the state at the same index in the state list
The rewards correspond to the reward received by taking this action and arriving at the same index in the state list
'''

from random import randint

#contains a list of states and action objects
class Domain():
	def __init__(self, states, actions):
		self.states = states
		self.actions = actions

	def setActions():
		pass

#This represents a state in the scenario, it is comprised of a name and set of actions
#no information about the state is required pther than the actions available to take from it
class State():
	def __init__(self,name,actions):
		self.actions = actions
		self.name = name

	def __repr__(self):
		#return str(self.name) + ", " +str(self.actions) 
		return "s"+str(self.name)
	
	def display(self):
		print str(self.name) + ", " +str(self.actions) 


#This represents an actions available to the agent
#It takes three lists, where outomes is a list of states which are possible outcomes from the action
#probs, which are the probabilities of arising the in the correspondingly indexed state given this action
#rewards, the reward obtained by ariving in the corresponding state given this action
class Action():
	def __init__(self,name,outcomes,probs,rewards):
		self.name = name
		self.outcomes = outcomes
		self.probs = probs
		self.rewards = rewards
	def __repr__(self):
		return "a"+str(self.name)

	def display(self):
		print str(self.name) + ", "+ str(self.outcomes) +", "+str(self.probs)+ ", "+ str(self.rewards)

def generate(stateN, actionN, tstateN, minOperA, maxOperA, AperS):
	domain = Domain([],[])
	#generate states
	

	for i in range(stateN):
		domain.states.append(State(i, []))

	for i in range(actionN):
		action = Action(i, [], [], [])
		
		actionOutcomes = []
		actionProbs = []
		actionRewards = []

		outcomeN = randint(minOperA, maxOperA)
		for j in range(outcomeN):
			rstate = randint(0, stateN-1)

			#print rstate
			#print len(domain.states)

			while domain.states[rstate] in action.outcomes:	#dont readd outcomes which are alreayd outcomes
				rstate = randint(0, stateN-1)
			action.outcomes.append(domain.states[rstate])	#add a random state outcome

			action.probs.append(1.0/outcomeN)#if two outcomes, will always be 0.5, 0.5, this should be made more complex
			action.rewards.append(randint(-50,50))

			if(domain.states[rstate] == domain.states[stateN-1]):	#tis is the final terminal state, make the goal state
				action.rewards[j] = 100

			if(domain.states[rstate] == domain.states[stateN-2]):	#tis is the penultimate t state, make the fail state
				action.rewards[j] = -100
		
		domain.actions.append(action)

	for i in range(stateN - (tstateN)):	#add actions to all states bar the terminal states
		for j in range(AperS):
			raction = randint(0, actionN-1)
			while domain.actions[raction] in domain.states[i].actions:
				raction = randint(0, actionN-1)
			domain.states[i].actions.append(domain.actions[raction])

	print "Domain\n\nStates"
	for s in domain.states:
		s.display()
	print "Actions"
	for a in domain.actions:
		a.display()
	return domain

#d = generate(5,5,1,1,2,2,3)
