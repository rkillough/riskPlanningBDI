'''
This implementation consists of a UCB1 based algorithm which (unlike plain UCT) handles both probabilistic outcomes and unrestricted rewards (as opposed to [0,1]).

The scenario privided is a single robot navigation problem. The robot must choose between routes toward an end goal over bridges of varying widths.
'''


from __future__ import division
import random
import math

#This represents a state in the scenario, it is comprised of a name and set of actions
#no information about the state is required pther than the actions available to take from it
class state():
    def __init__(self,name,actions):
        self.actions = actions
        self.name = name
        
#This represents an actions available to the agent
#It takes three lists, where outomes is a list of states which are possible outcomes from the action
#probs, which are the probabilities of arising the in the correspondingly indexed state given this action
#rewards, the reward obtained by ariving in the corresponding state given this action
class action():
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
s0 = state("s0",[])
s1 = state("s1",[])
s2 = state("s2",[])
s3 = state("s3",[])
s4 = state("s4",[])
s5 = state("s5",[])
s6 = state("s6",[])

#actions
a0 = action("a0", [s2,s6], [0.4,0.6], [-5,-100])
a1 = action("a1", [s1,s6], [0.8,0.2], [30,-100])
a2 = action("a2", [s5,s6], [0.1,0.9], [100,-100])
a3 = action("a3", [s3,s6], [0.99,0.01], [-10,-100])
a4 = action("a4", [s5,s6], [0.6,0.4], [100,-100])
a5 = action("a5", [s2,s6], [0.95,0.05], [-10,-100])
a6 = action("a6", [s3,s6], [0.6,0.4], [-10,-100])
a7 = action("a7", [s4,s6], [0.9,0.1], [-5,-100])
a8 = action("a8", [s5,s6], [0.8,0.2], [100,-100])
a9 = action("a9", [s5,s6], [0.98,0.02], [80,-100])
a10 = action("a10", [s0,s6], [0.8,0.2], [-30,-100])
a11 = action("a11", [s0,s6], [0.4,0.6], [-5,-100])
a12 = action("a12", [s1,s6], [0.99,0.01], [-10,-100])
a13 = action("a13", [s2,s6], [0.9,0.1], [-5,-100])

s0.actions = [a0,a1]
s1.actions = [a2,a3,a10]
s2.actions = [a6,a7,a11]
s3.actions = [a4,a5,a12]
s4.actions = [a8,a9,a13]
s5.actions = []   # This is the goal state
s6.actions = []   # This is the fail state




