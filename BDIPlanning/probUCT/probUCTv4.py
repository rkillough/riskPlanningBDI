'''
This implementation consists of a UCB1 based algorithm which (unlike plain UCT) handles both probabilistic outcomes and unrestricted rewards (as opposed to [0,1]).

The scenario privided is a single robot navigation problem. The robot must choose between routes toward an end goal over bridges of varying widths.

This particulr version implement accurate, non biased variance calculation (as well as discounting)
We also made the mistake in previous  version that while we were just ocnsidering immediate risk, we should have been using the backpropagated utility values for the calcultion
'''


from __future__ import division
from random import *
import math
import riskAwareDecision
import riskDecisionMaxMin
from copy import deepcopy

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

'''
Here we construct the states and actions of the scenario
All these items are globally avaialble to the algorithm

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

a0 = Action("a0", [s1,s2], [.5,.5], [2,2])
a1 = Action("a1", [s2], [1], [2])

a2 = Action("a2", [goal,fail], [.7,.3], [20,-10])
a3 = Action("a3", [goal,fail], [.5,.5], [10,-5])
a4 = Action("a4", [goal,fail], [.5,.5], [5,-2])



def SetActions():
	s0.actions = [a0,a1]
	s1.actions = [a2]
	s2.actions = [a3,a4]


def printTree(parent, indent):
	#print "XX:"+str(parent)
	print indent + str(parent) + " Utility/Visits:" + str(parent.utility)+"/"+str(parent.visits)
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
											


#This is wrapper around a State class instance to provide methods for its manipulation but allow the state to be easily changed
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
		self.risk = None	#currently modelled as plain variance
	
		self.depth = 0	#the current depth of the node in the tree

		if self.nodetype == Nodetype.decision:
			self.actions = deepcopy(state.GetActions())
			self.untriedActions = deepcopy(state.GetActions())
		
		
	#Select a child node using the UCB1 formula
	def SelectChild(self):
		C = exploreBias		#Exploration exploitation tradeoff constant
		#print "Vals: "+str(n.utility) + " " + str(n.visits) +" "+ str(self.visits)
		s = sorted(self.children, key = lambda n: n.utility/n.visits + C* math.sqrt(2*math.log(self.visits)/n.visits))
		return s[-1]
		#find the highest valued child node

	def RandomAction(self):
		actions = self.actions
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
	def AddChild(self, Caction, Cstate, nodetype):
		childNode = Node(action=Caction, parent=self, state=Cstate, nodetype=nodetype)
		
		print "Adding new node!"
		print "i:"+str(childNode)
		for c in self.children:
			print c
		print "---------"
		self.children.append(childNode)
		#self.untriedActions.remove(Caction)

		return childNode

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
def UCT(rootState, i, gamma, R):
	rootNode = Node(state=rootState, nodetype=Nodetype.decision)

	#depth = 0

	for i in range(i):
		#Initialise
		node = rootNode
		state = rootState

		depth = 0

		#Select a new node oce all actions have been tried
		#print node
		#should enter here on decsion node
		while node.untriedActions == [] and node.children != []:
			print "selecting from children of "+str(node) + str(node.children)
			print node.visits
			for c in node.children:
				print c.visits
			node = node.SelectChild()
			#print "outcome "+str(node) + str(node.children)

			#weve selected a new decision node but we need ot end up in a chance node, so select a random one		
			if node.children == []:
				#print "No child decision nodes, create one and move there"
				newState = GetOutcome(node.action)
				node = node.AddChild(None, newState, nodetype=Nodetype.decision)
			else:
				#print "moving to child decision node"
				#print node.children
				node = node.GetRandomChild()
			
			depth += 1


		#Expand randomly through the tree while there are untried actions
		#if node.nodetype == Nodetype.decision:		#this may be unecessary as it should always be anyway
		
		if(node.actions != []):	#if not a terminal decision node

			randomAction = node.RandomAction()
			newState = node.state.DoAction(randomAction)

			dnodeexists = False			#only add a new decision node if this node hasn't been sampled yet
			for c in node.children:
				if c.action == randomAction: # action has a node here, so move to that node in case we sample a new outcome
					node = c			
					dnodeexists = True
					
					cnodeexists = False	#now check if the state we sampled already exists as a chance node
					for c in node.children:
						#print "\t\t"+str(c.state.currentState.name) + " "+str(newState.currentState.name)
						if c.state.currentState.name == newState.currentState.name:
							cnodeexists = True	#this state already been sampled, don't go to this node
							node = node.parent
					if not cnodeexists:	#this state hasnt been sampled yet, add a new decison node
						print "Adding new child decision "+str(newState.currentState.name)+" node to exisitng chance node "+str(node)
						node = node.AddChild(None, newState, nodetype=Nodetype.decision)
					

			if not dnodeexists:	#this is a new action which hasnt been sampled, so that state will definitely be new, add two new nodes, a chance a decision
				for a in node.untriedActions:
					if a.name == randomAction.name:
						node.untriedActions.remove(a)	#indicate that this action has now been tried atleast once
				#print "Adding new chance and decision node"
				node = node.AddChild(randomAction, None, nodetype=Nodetype.chance)
				node.depth = depth
				node = node.AddChild(None, newState, nodetype=Nodetype.decision)
				

		#This should never happen, but leave in for testing	
		elif node.nodetype == Nodetype.chance:		#This means weve just selected a new chance node in the select
			print "this shouldnt happen"
			if node.children == []:
				newState = node.state.DoAction()
				node = node.AddChild(None, newState, nodetype=Nodetype.decision)
			else:
				node = node.GetRandomChild()
		

		
		#Rollout, carry out a random walk through the tree untila  terminal state is reached
		while node.children != []:	
			node = node.GetRandomChild()	#get a random action
			node = node.GetRandomChild()	#get random decision node
		
					
		#Backpropogate the cumulative reward and risk back up through the tree
		cumulativeReward = 0
		cumulativeRisk = 0

		while node != None and node.parent != None:	#while we havent gone above the root of the tree

			state = node.state.currentState
			#get state (this will initially be a leaf node, or the deepest we traversed in rollout)
			node.AddVisit()
			node = node.parent	#go to parent (chance node) to get action
			action = node.action
			reward = GetReward(state, action)	 #get reward obtained for taking the action and arriving in the state 
			print "Got "+str(reward)+" for taking "+action.name+" and arriving in "+state.name

			cumulativeReward += reward * (gamma ** node.depth)
			node.AddVisit()
				
			mean, M2, risk = calculateRisk(node.visits, node.mean, node.M2, reward)

			#Check if risk is lower than risk of siblings
			if cumulativeRisk is not None:
				cumulativeRisk += risk
				node.Update(cumulativeReward, mean, M2, cumulativeRisk)
			
			isSmallest = True
			if node.parent:
				for n in node.parent.children:
					if cumulativeRisk > n.risk:
						cumulativeRisk = None  #this path has a higher risk than alternatives,dont update risk from this path
			node = node.parent
			if node.parent == None:
				node.AddVisit()
		


	#sort the list of root child nodes by their utility
	#actionList = sorted(rootNode.children, key= lambda c: c.utility/c.visits, reverse=True)
	
	#sort the list by the desired metric (should be utility in the final version ... utility/visits)
	actionList = sorted(rootNode.children, key= lambda c: (c.utility/c.visits), reverse=True)

	'''
	for a in actionList:
		print str(a)
		for n in a.children:
			
			print "\t"+str(n) 
			for m in n.children:
				print "\t\t"+str(m)
	'''
	for a in actionList:
		printTree(a, '')

	decision = riskDecisionMaxMin.pickAction(actionList, R)

	print "\nDecision:"
	return decision		#USe the decision rule
	#return actionList[0]				#Just use utility


SetActions()
initialState = StateWrapper(s0)
currentState = initialState

iters = 1000
gamma = 1
R = 0
exploreBias = 100

print "\nRunning UCT with parameters:\nIterations: "+str(iters)
print "Discount: "+str(gamma)
print "Risk value: "+str(R)+"\n"

print UCT (currentState, iters, gamma, R)

#print playScenario(gamma,R)

print "\n"
