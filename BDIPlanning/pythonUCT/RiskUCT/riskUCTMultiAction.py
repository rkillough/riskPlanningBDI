#i This is a very simple implementation of the UCT Monte Carlo Tree Search algorithm in Python 2.7.
# The function UCT(rootstate, itermax, verbose = False) is towards the bottom of the code.
# It aims to have the clearest and simplest possible code, and for the sake of clarity, the code
# is orders of magnitude less efficient than it could be made, particularly by using a 
# state.GetRandomMove() or state.DoRandomRollout() function.
# 
# Example GameState classes for Nim, OXO and Othello are included to give some idea of how you
# can write your own GameState use UCT in your 2-player game. Change the game to be played in 
# the UCTPlayGame() function at the bottom of the code.
# 
# Written by Peter Cowling, Ed Powley, Daniel Whitehouse (University of York, UK) September 2012.
# 
# Licence is granted to freely use and distribute for any sensible/legal purpose so long as this comment
# remains in any distributed code.
# 
# For more information about Monte Carlo Tree Search check out our web site at www.mcts.ai

'''
This is the same as riskUCT except the scenario has more action options from each state. Before we only had two optionsfrom each state, here we include more actins to effectively allow movement between any adjacent state (including going backwards)
'''


from math import *
import random
import calculateRisk

T = -100000     #utility tolerance threshold, this ws formerly relative tot he utility of the the top action, but this does not work for negative utilities, so it is simply an absolute value which is set by the BDI agent, actions must have higher utilities than this to be returned

class AssessedAction():
    def __init__(self,a,u,r):
        self.action = a
        self.utility = u
        self.risk = r


class state():
    def __init__(self,name,actions):
        self.name = name
        self.actions = actions
    
    def __repr__(self):
        return self.name


class action():
    #three lists
    #outcomes: a list of states
    #probs: a list of the probabilties of the index corresponding state being the outcome
    #rewards: a list of the reward received if we arrive in the index corresponding state
    def __init__(self,name,outcomes,probs,rewards):
        self.name = name
        self.outcomes = outcomes
        self.probs = probs
        self.rewards = rewards

    def __repr__(self):
        return self.name
        

#construct nuclear scenario
s0 = state("s0",[])
s1 = state("s1",[])
s2 = state("s2",[])
s3 = state("s3",[])
s4 = state("s4",[])
s5 = state("s5",[])
s6 = state("s6",[])

a0 = action("a0", [s2,s6], [0.4,0.6], [-5,-100])
a1 = action("a1", [s1,s6], [0.8,0.2], [-30,-100])
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

def setActions():
    s0.actions = [a0,a1]
    s1.actions = [a2,a3,a10]
    s2.actions = [a6,a7,a11]
    s3.actions = [a4,a5,a12]
    s4.actions = [a8,a9,a13]
    #s5.actions = []	This is the goal state
    #s6.actions = []	This is the fail state

#return a "random" state based on the probabilties of the actions' outcomes
def getOutcome(a):
	r = random.randint(0,999)	#this function ignores some precision for probabilities with more than 3 dp of precision, probably a better way to do it than this
	#print "R: "+str(r)
	distribution = []
	l = 0	#lower bound
	t = 0	#cumulative probability
	for p in a.probs:
		distribution.append([l, ((t+p)*1000)+1]) #this list is the lower and upper bounds in the distribution
		l = (p*1000)
		t = t+p

	for i in range(len(a.outcomes)):
		if(r>=distribution[i][0] and r<distribution[i][1]):
			return a.outcomes[i]

    #return cState #this implies there are no outcomes because there are no actions to take (e.g. s5 or s6)


#new state with uncertainty
class nuclearState():
    """
    This state models a simple mobile robot moving toward a goal state
    There are a set of motion paths which can be taken to move toward the goal state, each with different probabilities
    of success (which means there is uncertainty about the outcomes)
    """ 
    def __init__(self, cState):
        self.currentState = cState
        
    def Clone(self):
        st = nuclearState(self.currentState)
        
        return st

    #take the action
    def DoMove(self, action):
        #print "Doing : "+str(action)
        self.currentState = getOutcome(action)
        #print "State outcome: "+str(self.currentState)

    #return list of available actions
    def GetMoves(self):
        #aa = ""
        #for a in self.currentState.actions:
        #    aa = aa+str(a)
        #print "Available actions: "+aa
        #print self.currentState
        return self.currentState.actions

    def GetRandomMove(self):
        moves = self.GetMoves()
        r = random.randint(1,len(moves)) -1
        return moves[r]

    #return immediate reward 
    def GetResult(self, state, action):
        reward = 0
        if(action is not None):         #the root node will be None (we didnt take an action to reach it))
            for i in range(len(action.outcomes)):
                if(action.outcomes[i] == state):
                    reward = action.rewards[i]

        #print "Reward: "+str(reward)
        #print "GetResult: "+str(state)+","+str(action)+","+str(reward)
        return reward 

    def __repr__(self):
        return self.currentState.name	

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.utility = 0 #formerly just wins, we want a more complex measure of utility which is discounted 
        self.visits = 0
    
        self.mean = 0  #the running mean utility
        self.variance = 0 #the running loss-only variance

        self.untriedMoves = state.GetMoves() # future child nodes
        self.state = state.currentState
        
        #self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        
        #NOTE: as mentioned above, we are unable to alter the e/e bias without adding a constant UCTK (reffered to in the paper as Cp where Cp>0.
        
        UCTK = 1000

        #c.utility/c.visits is effectively the average reward over the visitations   
        #UCTK is as above and folowwing that is the biasing calculation
        #s = sorted(self.childNodes, key = lambda c: c.utility/c.visits + UCTK* sqrt(2*log(self.visits)/c.visits))[-1]
        
        #for testing/understanding
        s = sorted(self.childNodes, key = lambda c: c.utility/c.visits + UCTK* sqrt(2*log(self.visits)/c.visits))

        #print "Current node:"+str(self.state)+str(self.move)
        #for c in s:
        #    print "child node: "+str(c)            
        #print "---------------------------------"
        #print "Select child: "+str(s) 
        return s[-1]
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. 
            Also update the mean and the variance(risk) of the node
        """
        self.visits += 1
        #print "Result: "+str(self.move) + ":"+str(result)
        self.utility += result

        #Update variance and mean calculations using the calculaterisk class
        #+1 is added to childnodes to represent a dummy zero value required by the loss only variance calculation (not currently in use)

        self.mean, self.variance = calculateRisk.updateVariance(len(self.childNodes), self.mean, self.variance, result)
        #print "LOVAR: "+str(self.LOvariance)
        

    def __repr__(self):
        return "[Action:" + str(self.move) + " Utility/Visits:" + str(self.utility) + "/" + str(self.visits) +" = "+ str(self.utility/self.visits) + " Mean/Variance:" + str(self.mean) + "/" + str(self.variance) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        #print "SELECT"
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal and state arrived at is non terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)
            node.state = state.currentState

        #print"EXPAND"
        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree

        #print"ROLLOUT"
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            move = state.GetRandomMove()
            state.DoMove(move)

        #print "BACKPROPOGATE"
        # Backpropagate
        result = 0
        while node != None: # backpropagate from the expanded node and work back to the root node
            result += state.GetResult(node.state, node.move) 
            #print "BackPropogating: "+str(node.state) + str(node.move) + " with value " + str(result)
            node.Update(result) # state is terminal. Update node with result 

            node = node.parentNode

        #print "-------------------------------------------------------------------------------------"+str(i)

    # Output some information about the tree - can be omitted
    if (verbose): print rootnode.TreeToString(0)
    else: print rootnode.ChildrenToString()

    #return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
    actionlist = sorted(rootnode.childNodes, key = lambda c: c.utility, reverse=True)
    #Note, the list is generally sorted ascending and the last action taken, we sort descending and take the first

    #create a list of assessed actions from the list of nodes and remove actions with utility below the threshold
    aalist = []

    #add first item because we always want at least one return and its needed for comparison for additional returns
    utility = actionlist[0].utility 
    risk = actionlist[0].variance
    x0 = AssessedAction(actionlist[0].move, utility, risk) #0 for risk because we dont have a value yet
    aalist.append(x0)
    
    for x in actionlist[1:]:    
        
        utility = x.utility 
        risk = x.variance
        
        if(utility > T):     #node utility passes threshold, make an AA
            xi = AssessedAction(x.move, utility, risk)
            aalist.append(xi)
    
    return aalist

#print out an assessed action list in a nice format
def PrintAAList(l):
    for x in l:
        print "Action: "+str(x.action)+"\tUtility: "+str(x.utility)+"\tRisk: "+str(x.risk)


#Make an iterated attempt to reach the goal, return 1 if successful
def attempt():
    setActions()         #this must be done after each iteration of uct as the algorithm deletes available actions
    state = nuclearState(s0)
    
    while(state.GetMoves() != []):
        results = UCT(rootstate =state, itermax=1000)    
        PrintAAList(results)

        #"actually" do the best action and proceed to the next state
        print "Doing "+results[0].action.name
        nextState = getOutcome(results[0].action)
        print "Outcome "+nextState.name

        setActions()

        state = nuclearState(nextState)
        print "Options: "+str(state.GetMoves())
        print "--------------------------------------------"
                        
    if(state.currentState.name == "s5"):
        print "Success! the goal was reached"
        return 1
    else:
        print "Failure! the robot fell in the pit"
        return 0



if __name__ == "__main__":
 

    ''' Play the scenario out Iter times and measure how often we are successful
        The returned actions are ranked by visits, the utility is the cumulative reward/visits
        Here we simply choose the highest action by utility to proceed with
        
    '''
    successCount = 0
    Iter = 100

    for i in range(Iter):
        successCount += attempt()
        print 
        print "##################################################"
        print
    
    print "\nSuccess rate: "+ str(successCount)
    
    
    #attempt()        
