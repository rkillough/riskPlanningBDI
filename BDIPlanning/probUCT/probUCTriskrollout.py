'''
This implementation consists of a UCB1 based algorithm which (unlike plain UCT) handles both probabilistic outcomes and unrestricted rewards (as opposed to [0,1]).

The scenario privided is a single robot navigation problem. The robot must choose between routes toward an end goal over bridges of varying widths.

'''


from __future__ import division
from random import *
import math
import riskAwareDecision
import riskDecisionMaxMin
from copy import deepcopy
from datetime import datetime

exploreBias = 0

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

class Nodetype:
	decision, chance = range(2)


#Here we construct the states and actions of the scenario
#all these items are globally avaialble to the algorithm
#'''
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
a3 = Action("a3", [s3,s6], [0.99,0.01], [-20,-100])
a4 = Action("a4", [s5,s6], [0.4,0.6], [100,-100])
a5 = Action("a5", [s2,s6], [0.95,0.05], [-20,-100])
a6 = Action("a6", [s3,s6], [0.95,0.05], [-20,-100])
a7 = Action("a7", [s4,s6], [0.9,0.1], [-5,-100])
a8 = Action("a8", [s5,s6], [0.8,0.2], [100,-100])
a9 = Action("a9", [s5,s6], [0.95,0.05], [65,-100])
a10 = Action("a10", [s0,s6], [0.8,0.2], [-30,-100])
a11 = Action("a11", [s0,s6], [0.4,0.6], [-5,-100])
a12 = Action("a12", [s1,s6], [0.95,0.05], [-10,-100])
a13 = Action("a13", [s2,s6], [0.9,0.1], [-5,-100])

def SetActions():
    s0.actions = [a0,a1]
    s1.actions = [a2,a3,a10]
    s2.actions = [a6,a7,a11]
    s3.actions = [a4,a5,a12]
    s4.actions = [a8,a9,a13]
    s5.actions = []   # This is the goal state
    s6.actions = []   # This is the fail state
'''

#Example tree for testing
s0 = State("s0", [])
s1 = State("s1", [])
s2 = State("s2", [])

fail = State("fail", [])
goal = State("goal", [])

a0 = Action("a0", [s1,s2], [.9,.1], [2,-10])
a1 = Action("a1", [s2], [1], [2])

a2 = Action("a2", [goal,fail], [.7,.3], [20,-10])
a3 = Action("a3", [goal,fail], [.5,.5], [10,-5])
a4 = Action("a4", [goal,fail], [.5,.5], [5,-2])

def SetActions():
	s0.actions = [a0,a1]
	s1.actions = [a2]
	s2.actions = [a3,a4]


#Kims issue proof example
s0 = State("s0", [])
s1 = State("s1", [])
s2 = State("s2", [])
s3 = State("s3", [])
s4 = State("s4", [])
s5 = State("s5", [])
s6 = State("s6", [])
s7 = State("s7", [])
s8 = State("s8", [])
s9 = State("s9", [])
s10 = State("s10", [])
s11 = State("s11", [])
s12 = State("s12", [])
s13 = State("s13", [])
s14 = State("s14", [])
s15 = State("s15", [])
s16 = State("s16", [])
s17 = State("s17", [])
s18 = State("s18", [])
s19 = State("s19", [])
s20 = State("s20", [])

a0 = Action('a0', [s1,s2], [.5,.5], [0,0])
a1 = Action('a1', [s3,s4], [.5,.5], [0,0])

a2 = Action('a2', [s5,s6], [.5,.5], [100,100])
a3 = Action('a3', [s7,s8], [.5,.5], [-100,-100])
a4 = Action('a4', [s9,s10], [.5,.5], [100,100])
a5 = Action('a5', [s11,s12], [.5,.5], [-100,-100])

a6 = Action('a6', [s13,s14], [.5,.5], [50,-50])
a7 = Action('a7', [s15,s16], [.5,.5], [50,-50])
a8 = Action('a8', [s17,s18], [.5,.5], [50,-50])
a9 = Action('a9', [s19,s20], [.5,.5], [50,-50])

def SetActions():
	s0.actions = [a0,a1]
	s1.actions = [a2,a3]
	s2.actions = [a4,a5]
	s3.actions = [a6,a7]
	s4.actions = [a8,a9]
'''

#display info about the node
def printNode(n):
	if n.nodetype == Nodetype.chance:
		tUtil = n.utility
		visits = n.visits
		tRisk = n.risk		
		utility = 0
		risk = 0
		if(visits > 0):		#if there are no visits to the node, things will break due to division by zero, so..
			utility = round(tUtil/visits,2) 
			risk = round(tRisk/visits,2)
		return str(n) + "\tU/V:" + str(tUtil)+"/"+str(visits)+"="+str(utility)+"\tRisk:"+str(risk)
	else:
		return str(n) + " visits:"+str(n.visits)


#recursivley print the whole tree given the root node
def printTree(parent, indent):
	#print "XX:"+str(parent)
	print indent + printNode(parent)
	indent += "____"
	for n in parent.children:
		#print "X:"+str(n)
		printTree(n, indent)


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


#Return the immediate reward of taking action and arriving in state
def GetReward(state, action):
    reward = 0
    for i in range(len(action.outcomes)):   #verify that state is an outcome of action
        if(action.outcomes[i] == state):
            reward = action.rewards[i]		#if so, return the reward for arriving in state given action
    return reward


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
											

#This is wrapper around a State class instance to provide methods for its manipulation but allow the current state to be easily changed
class StateWrapper():
    def __init__(self,cState):
        self.currentState = cState

    def DoAction(self, action):
        return StateWrapper(GetOutcome(action))

    def GetActions(self):
        return self.currentState.actions

    def GetRandomAction(self):
        actions = self.GetActions()
        r = randint(1,len(actions)) -1
        return actions[r]

	def __repr__(self):
		return self.currentState.name

#A UCT node modified to include mean and variance
class Node:
	def __init__(self, action=None, parent=None, state=None, nodetype=None):
		self.action = action
		self.state = state
		self.parent = parent
		self.children = []
		self.nodetype = nodetype
		self.utility = 0
		self.visits = 0
		self.mean = 0
		self.M2 = 0
		self.risk = 0	#currently modelled as plain variance
		self.depth = 0	#the current depth of the node in the tree

		if self.nodetype == Nodetype.decision:
			self.actions = deepcopy(state.GetActions())
			self.untriedActions = deepcopy(state.GetActions())
		
	#Select a child node using the UCB1 formula
	def SelectChild(self):
		C = exploreBias		#Exploration exploitation tradeoff constant
		s = sorted(self.children, key = lambda n: n.utility/n.visits + C* math.sqrt(2*math.log(self.visits)/n.visits))
		return s[-1]

	def RandomAction(self):
		actions = self.actions
		r = randint(1,len(actions)) -1
		return actions[r]

	def AddVisit(self):
		self.visits += 1

	def UpdateReward(self, reward):
		self.utility += reward

	def UpdateRisk(self, mean, M2, risk):
		self.mean = mean
		self.M2 = M2
		self.risk += risk

	#A new sample has been taken, add this as a child node to this node
	def AddChild(self, Caction, Cstate, nodetype):
		childNode = Node(action=Caction, parent=self, state=Cstate, nodetype=nodetype)
		self.children.append(childNode)
		return childNode

	#return a child decision node based on the probability of occurance
	def SimulateAction(self):
		outcome = GetOutcome(self.action)
		for c in self.children:
			if(outcome.name == c.state.currentState.name):
				return c

	#return a purely random child node
	def GetRandomChild(self):
		n = len(self.children)	
		r = randint(0,n-1)
		return self.children[r]

	def __repr__(self):
		if self.nodetype == Nodetype.decision:
			return "Decision: "+ self.state.currentState.name
		else:
			return "Chance: "+ self.action.name
	

#Takes a root state, an iter depth, a discount factor and a risk tolerance factor
def UCT(rootState, iters, gamma, horizon, R, rolloutCount):
	rootNode = Node(state=rootState, nodetype=Nodetype.decision)

	for i in range(iters):
		#Initialise
		node = rootNode
		depth = 0

		#Select a new node once all actions have been tried
		while node.untriedActions == [] and node.children != []:
			node = node.SelectChild()
			node = node.SimulateAction()
			depth += 1

		#Expand randomly through the tree while there are untried actions
		if node.untriedActions != [] and depth<horizon:	#if not a terminal decision node or too deep in the tree
			randomAction = node.RandomAction()
			dnodeexists = False			#only add a new decision node if this node hasn't been sampled yet
			for c in node.children:
				#print "XX: "+str(c.action.name)+ " "+str(randomAction.name)
				if c.action.name == randomAction.name: # action has a node here, do nothing
					dnodeexists = True
			if not dnodeexists:	#this is a new action which hasnt been sampled, we add nodes for every state outcome
				#indicate that this action has now been tried atleast once
				for a in node.untriedActions:
					if a.name == randomAction.name:
						node.untriedActions.remove(a)
				#Adding new chance node
				node = node.AddChild(randomAction, None, nodetype=Nodetype.chance)
				node.depth = depth
				#adding node for each outcome of this action
				for outcome in node.action.outcomes:
					node.AddChild(None, StateWrapper(outcome), nodetype=Nodetype.decision)
				#randomly select from these outcomes (dont do this until riskrollout complete)
				node = node.GetRandomChild()
		
		#ROLLOUT PHASE
		state = node.state

		#Risk rollout, randomly sample a set of decision nodes from the last chance node to give an approximation of the risk, only do this if the node has never been sampled and thus has a totally innacurate risk assessment
		if node.parent != None:	
			node = node.parent	#move to parent node
			#print str(node) +", "+ str(node.visits)
			if node.visits == 0:	#only consider non visited nodes
				node.AddVisit()		#add a single visit
				action = node.action		#get the action
				for i in range(rolloutCount):
					outcomenode = node.SimulateAction()		#sample a state outcome
					outcomestate = outcomenode.state.currentState
					reward = GetReward(outcomestate, action)	#get the reward for this state sample
					mean, M2, risk = calculateRisk(i+1, node.mean, node.M2, reward)	
					node.UpdateRisk(mean, M2, risk)					#get risk and update node
					#print "Updating risk of "+str(node)+ " with "+ str(reward)
				#print printNode(node)
				node.risk = node.risk/rolloutCount	#important: normalise cumul risk as if wed only sampled once
				node.M2 = 0
				node.mean = 0
				#print printNode(node)
			node = node.SimulateAction()	#move to a random decision node for next stage of rollout
		

		#Rollout, carry out a random walk through the tree until a terminal state		
		rolloutReward = 0	#since we have intermediate rewards, we need to accumalate these in the rollout
		while state.GetActions() != []:	
			action = state.GetRandomAction()
			state =	state.DoAction(action)
			depth += 1 
			rolloutReward += GetReward(state.currentState, action) * (gamma ** depth)
				

		#Backpropagate the cumulative reward and risk back up through the tree
		cumulativeReward = 0
		cumulativeRisk = 0
		while node != None and node.parent != None:	#while we havent gone above the root of the tree
			state = node.state.currentState
			#get state (this will initially be a leaf node, or the deepest we traversed in expansion)
			node.AddVisit()
			node = node.parent	#go to parent (chance node) to get action
			action = node.action

			node.AddVisit()
			reward = GetReward(state, action)	 #get reward obtained for taking the action and arriving in the state
			#We update the risk only using the immediate reward, rather than that plus the rollout reward
			mean, M2, risk = calculateRisk(node.visits, node.mean, node.M2, reward)
			cumulativeRisk += risk * (gamma ** node.depth)

			reward += rolloutReward 		#add the reward from the simultion (rollout) of lower states (if any) before updateing the nodes reward
			cumulativeReward += reward * (gamma ** node.depth)	
			node.UpdateRisk(mean, M2, cumulativeRisk)	
			noderisk = cumulativeRisk

			#we want to determien the lowest risk sibling, but risk will be zero for unsampled or low sampled nodes, construct a list of nodes we know have been sampled a few times
			sampledNodes = []
			for n in node.parent.children:
				#Dont consider low sampled actions or the current action for comparison
				if n.visits > 0 and n.action.name != node.action.name:	
					sampledNodes.append(n)
			if sampledNodes != []:
				lowestRiskSibling = sorted(sampledNodes, key = lambda r: r.risk/r.visits)[-1]
				riskofLRS = lowestRiskSibling.risk/lowestRiskSibling.visits
				#print str(noderisk) + ">" +str(n.risk/n.visits)
				if noderisk > riskofLRS:	#There is a path which has lower risk, BP that instead
					cumulativeRisk = riskofLRS 
		
			node.UpdateReward(cumulativeReward)

			node = node.parent
			if node.parent == None:
				node.AddVisit()
		

	#sort the list of root child nodes by their utility
	actionList = sorted(rootNode.children, key= lambda c: (c.utility/c.visits), reverse=True)

	#Print the whole tree
	'''
	print "\n\n"
	for a in actionList:
		printTree(a, '')
	#'''
	#print "\nOptions:"
	#for a in actionList:
	#	print printNode(a)

	#Make a decision
	decision = riskDecisionMaxMin.pickAction(actionList, R)
	
	#print "\nDecision:\n"+printNode(decision)
	return decision		#USe the decision rule
	#return actionList[0]				#Just use utility


def runUCT(initState, iters, gamma, R, eb, horizon, rolloutCount):

	initialState = StateWrapper(initState)

	global exploreBias 
	exploreBias = eb

	#print "\nRunning UCT with parameters:\nIterations: "+str(iters)
	#print "Discount: "+str(gamma)
	#print "Risk value: "+str(R)+"\n"

	starttime = datetime.now()
	decision = UCT (initialState, iters, gamma, horizon, R, rolloutCount)
	endtime = datetime.now()
	
	#print "\nResults obtained in: "+str(endtime-starttime)
	SetActions()	
	return decision

SetActions()

'''
iters = 10000
gamma = 0.9
R = 0
exploreBias = 50
horizon = 10
rolloutCount = 10
'''
#runUCT(s4, iters, gamma, R, exploreBias, horizon, rolloutCount)


