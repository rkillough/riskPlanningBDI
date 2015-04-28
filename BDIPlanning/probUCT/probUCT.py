'''
This implementation consists of a UCB1 based algorithm which (unlike plain UCT) handles both probabilistic outcomes and unrestricted rewards (as opposed to [0,1]).

The scenario privided is a single robot navigation problem. The robot must choose between routes toward an end goal over bridges of varying widths.
'''


from __future__ import division
import random
import math

#This represents a state in the scenario, it is comprised of a name and set of actions
#no information about the state is required pther than the actions available to take from it
class State():
    def __init__(self,name,actions):
        self.actions = actions
        self.name = name
        
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
a1 = Action("a1", [s1,s6], [0.8,0.2], [30,-100])
a2 = Action("a2", [s5,s6], [0.1,0.9], [100,-100])
a3 = Action("a3", [s3,s6], [0.99,0.01], [-10,-100])
a4 = Action("a4", [s5,s6], [0.6,0.4], [100,-100])
a5 = Action("a5", [s2,s6], [0.95,0.05], [-10,-100])
a6 = Action("a6", [s3,s6], [0.6,0.4], [-10,-100])
a7 = Action("a7", [s4,s6], [0.9,0.1], [-5,-100])
a8 = Action("a8", [s5,s6], [0.8,0.2], [100,-100])
a9 = Action("a9", [s5,s6], [0.98,0.02], [80,-100])
a10 = Action("a10", [s0,s6], [0.8,0.2], [-30,-100])
a11 = Action("a11", [s0,s6], [0.4,0.6], [-5,-100])
a12 = Action("a12", [s1,s6], [0.99,0.01], [-10,-100])
a13 = Action("a13", [s2,s6], [0.9,0.1], [-5,-100])

s0.actions = [a0,a1]
s1.actions = [a2,a3,a10]
s2.actions = [a6,a7,a11]
s3.actions = [a4,a5,a12]
s4.actions = [a8,a9,a13]
s5.actions = []   # This is the goal state
s6.actions = []   # This is the fail state


#This method returns a 'random' probability adjusted state outcome given an action
def GetOutcome(action):
    r = random.randint(0,999)   #Note, this will ignore precision in probabilties with more than 3 dp
    distribution = []   #2d array of integer upper and lower bounds corresponding to the action's probabilties
    l = 0 #lower bound
    t = 0 #cumulative prob
    for p in a.probs:
        distribution.append([l, ((t+p)*1000)+1])
        l = p*1000
        t = t+p

    for i in range(len(a.outcomes)):
        if(r >= distribution[i][0] and r < distribution[i][1]):
            return a.outcomes[i]

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
        r = random.randint(1,len(actions)) -1
        return actions[r]

    #Return the immediate reward of taking action and arriving in state
    def GetResult(self, state, action):
        reward = 0
        if(action != None):     #handles root node which will have a null arrival action
            for i in range(len(action.outcomes)):   #verify that state is an outcome of action
                if(action.outcomes[i] == state)
                    reward = action.rewards[i]

        return reward

#A UCT node modified to include mean and variance
class Node:


    
