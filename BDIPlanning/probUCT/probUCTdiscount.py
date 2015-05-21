'''
This implementation consists of a UCB1 based algorithm which (unlike plain UCT) handles both probabilistic outcomes and unrestricted rewards (as opposed to [0,1]).

The scenario privided is a single robot navigation problem. The robot must choose between routes toward an end goal over bridges of varying widths.
'''


from __future__ import division
from random import *
import math
import riskAwareDecision
import riskDecisionMaxMin

#This represents a state in the scenario, it is comprised of a name and set of actions
#no information about the state is required pther than the actions available to take from it
class State():
    def __init__(self,name,actions):
        self.actions = actions
        self.name = name

	def __repr__(self):
		return self.name
        
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
		return self.name
	
'''
Here we construct the states and actions of the scenario
All these items are globally avaialble to the algorithm
'''

#states
s0 = State("s0",[])
s1 = State("s1",[])
s2 = State("s2",[])
s3 = State("s3",[])
s4 = State("s4",[])
s5 = State("s5",[])
s6 = State("s6",[])


#actions
a0 = Action("a0", [s2,s6], [0.4,0.6], [-5,-100])
a1 = Action("a1", [s1,s6], [0.9,0.1], [-30,-100])
a2 = Action("a2", [s5,s6], [0.1,0.9], [100,-100])
a3 = Action("a3", [s3,s6], [0.99,0.01], [-10,-100])
a4 = Action("a4", [s5,s6], [0.5,0.5], [100,-100])
a5 = Action("a5", [s2,s6], [0.95,0.05], [-10,-100])
a6 = Action("a6", [s3,s6], [0.6,0.4], [-10,-100])
a7 = Action("a7", [s4,s6], [0.9,0.1], [-5,-100])
a8 = Action("a8", [s5,s6], [0.8,0.2], [100,-100])
a9 = Action("a9", [s5,s6], [0.95,0.05], [65,-100])
a10 = Action("a10", [s0,s6], [0.8,0.2], [-30,-100])
a11 = Action("a11", [s0,s6], [0.4,0.6], [-5,-100])
a12 = Action("a12", [s1,s6], [0.99,0.01], [-10,-100])
a13 = Action("a13", [s2,s6], [0.9,0.1], [-5,-100])

def SetActions():
    s0.actions = [a0,a1]
    s1.actions = [a2,a3,a10]
    s2.actions = [a6,a7,a11]
    s3.actions = [a4,a5,a12]
    s4.actions = [a8,a9,a13]
    s5.actions = []   # This is the goal state
    s6.actions = []   # This is the fail state



#This method returns a 'random' probability adjusted state outcome given an action
def GetOutcome(action):
    r = randint(0,999)   #Note, this will ignore precision in probabilties with more than 3 dp
    distribution = []   #2d array of integer upper and lower bounds corresponding to the action's probabilties
    l = 0 #lower bound
    t = 0 #cumulative prob
    for p in action.probs:
        distribution.append([l, ((t+p)*1000)+1])
        l = p*1000
        t = t+p

    for i in range(len(action.outcomes)):
        if(r >= distribution[i][0] and r < distribution[i][1]):
            return action.outcomes[i]

#This in as online variance algorthm
#It maintains two running values in order to calcuate the variance
#The mean of all the rewards
#M2, which is the sum of squares of differences from the current mean
def calculateRisk(count, cMean, M2, newValue):

    delta = newValue - cMean
    mean = cMean + delta/count
    M2 = M2 + delta*(newValue - mean)
			
    if(count < 2):
        return mean, M2, 0
								
    variance = M2/(count-1)
    return mean, M2, variance
											


#This is wrapper around a State class instance to provide methods for its manipulation but allow the state to be easily changed
class StateWrapper():
    def __init__(self,cState):
        self.currentState = cState

    def DoAction(self, action):
        self.currentState = GetOutcome(action)

    def GetActions(self):
        return self.currentState.actions

    def GetRandomAction(self):
        actions = self.GetActions()
        r = randint(1,len(actions)) -1
        return actions[r]

    #Return the immediate reward of taking action and arriving in state
    def GetReward(self, state, action):
        reward = 0
        if(action != None):     #handles root node which will have a null arrival action (the root node)
            for i in range(len(action.outcomes)):   #verify that state is an outcome of action
                if(action.outcomes[i] == state):
                    reward = action.rewards[i]		#if so, return the reward for arriving in state given action

        return reward

#A UCT node modified to include mean and variance
class Node:
	def __init__(self, action=None, parent=None, state=None):
		self.action = action
		self.state = state.currentState
		self.parent = parent
		self.children = []
		
		self.utility = 0
		self.visits = 0
		
		self.mean = 0
		self.M2 = 0
		self.risk = 0	#currently modelled as plain variance
	
		self.untriedActions = state.GetActions()
		
	#Select a child node using the UCB1 formula
	def SelectChild(self):
		C = 600		#Exploration exploitation tradeoff constant
		s = sorted(self.children, key = lambda n: n.utility/n.visits + C* math.sqrt(2*math.log(self.visits)/n.visits))
		return s[-1]
		#find the highest valued child node
        '''
		topNode = None
		topValue = None

		for n in self.children:
			value = n.utility/n.visits + C * math.sqrt(2*math.log(self.visits/n.visits))
			if(value is None):
				topValue = value
				topNode = n
			elif(value > topValue):
				topValue = value
				topNode = n	
        '''

	def RandomUntriedAction(self):
		actions = self.untriedActions
		r = randint(1,len(actions)) -1
		return actions[r]

	def AddVisit(self):
		self.visits += 1

	def Update(self, reward, mean, M2, risk):
		self.utility += reward
		self.mean = mean
		self.M2 = M2
		self.risk = risk

	#A new sample has been taken, add this as a child node to this node
	def AddChild(self, Caction, Cstate):
		childNode = Node(action=Caction, parent=self, state=Cstate)
		self.children.append(childNode)
		self.untriedActions.remove(Caction)

		return childNode
		
	def __repr__(self):
		return "Action: "+ str(self.action.name) + " Utility = " + str(self.utility) + "/" + str(self.visits) + " = " + str(self.utility/self.visits) + " Risk = " + str(self.risk) + " Mean = " + str(self.mean)

#Takes a root state, an iter depth, a discount factor and a risk tolerance factor
def UCT(rootState, i, gamma, R):
	rootNode = Node(state = rootState)

	for i in range(i):
		#Initialise
		node = rootNode
		state = rootState
		depth = 0

		#Select a new node oce all actions have been tried
		while node.untriedActions == [] and node.children != []:
			node = node.SelectChild()
			state.DoAction(node.action)
			node.state = state.currentState

		#Expand randomly through the tree while there are untried actions
		if node.untriedActions != []:
			randomAction = node.RandomUntriedAction()
			state.DoAction(randomAction)
			node = node.AddChild(randomAction, state)

		#Rollout, carry out a random walk through the tree untila  terminal state is reached
		while state.GetActions() != []:
			depth+=1
			action = state.GetRandomAction()
			state.DoAction(action)

		#Backpropogate the cumulative reward and risk back up through the tree
		cumulativeReward = 0
		cumulativeRisk = 0
		while node != None:
			reward = state.GetReward(node.state, node.action)	 
			cumulativeReward += reward * (gamma ** depth)

			node.AddVisit()

			mean, M2, risk = calculateRisk(node.visits, node.mean, node.M2, reward)
			#cumulativeRisk += risk * (gamma ** depth)
			
			#just use immediate risk

			node.Update(cumulativeReward, mean, M2, risk)#cumulativeRisk)
			node = node.parent


	#sort the list of root child nodes by their utility
	#actionList = sorted(rootNode.children, key= lambda c: c.utility/c.visits, reverse=True)
	
	#sort the list by the desired metric (should be utility in the final version ... utility/visits)
	actionList = sorted(rootNode.children, key= lambda c: (c.utility/c.visits), reverse=True)


	#for a in actionList:
		#print "Action: "+str(a)
	
	#decision = riskAwareDecision.rankRiskAwareRatio(actionList, 1)
	#decision = riskAwareDecision.rankRiskAwareCI(actionList)
	#decision = riskAwareDecision.rankRiskAwareNormalisedComparison(actionList, 0.1)
	decision = riskDecisionMaxMin.pickAction(actionList, R)

	return decision		#USe the decision rule
	#return actionList[0]				#Just use utility

def playScenario(gamma, R):

	SetActions()
	initialState = StateWrapper(s0)
	currentState = initialState

	#UCT(currentState, 10000)

	success = 0		#this will remain 0 is failed, but be one if successful (s5 reached)
	rewardObtained = 0 #This, in this scenario, corresponds to the speed witht which the reactor was reached
	#More generally, it would correspond to the amount of critical resource consumed.

	#print "\n\n#################################################################################\n\n\n"	#for readability
	#Play out the scenario
	while (currentState.GetActions() != []):
		#plan and get the next best action
		bestAction = UCT(currentState, 1000, gamma, R)

		#print "Doing "+bestAction.action.name

		currentState.DoAction(bestAction.action)    #Actually 'do' the action
		rewardObtained += currentState.GetReward(currentState.currentState, bestAction.action)

		outcome = currentState.currentState.name
		#print "Outcome: "+outcome 
		if(outcome == 's5'):
			success = 1
		#print "---------------------------------------------------------------------------------------------\n"
		SetActions()    #This must be done after each planning phase as the algorithm removes these actions during planning

	#print "Total reward obtained: "+ str(rewardObtained)

	return success, rewardObtained


def iterateScenario(n, gamma, R):
	
	successCount = 0
	totalReward = 0
	
	for i in range(n):
		s, r = playScenario(gamma, R)
		successCount += s
		totalReward += r

	successProb = successCount/n
	avgReward = totalReward/n
	
	print "\n\n\n__________________________________________________________________________\n"
	print "Average Total Reward: "+str(avgReward)
	print "Probability of success: "+str(successProb)

	return avgReward, successProb
