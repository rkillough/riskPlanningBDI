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

from math import *
import random

T = 100     #100% utility tolerance threshold, this will just show all ranked results because were testing, but this can be lowered to reduce the number of results returned to the agent

class AssessedAction():
    def __init__(self,a,u,r):
        self.action = a
        self.utility = u
        self.risk = r



class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic 
        zero-sum game, although they can be enhanced and made quicker, for example by using a 
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    def __init__(self):
            self.playerJustMoved = 2 # At the root pretend the player just moved is player 2 - player 1 has the first move
        
    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved
        
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass



class OXOState:
    """ A state of the game, i.e. the game board.
        Squares in the board are in this arrangement
        012
        345
        678
        where 0 = empty, 1 = player 1 (X), 2 = player 2 (O)
    """
    def __init__(self):
        self.playerJustMoved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = [0,0,0,0,0,0,0,0,0] # 0 = empty, 1 = player 1, 2 = player 2
        
    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = OXOState()
        st.playerJustMoved = self.playerJustMoved
        st.board = self.board[:]
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerToMove.
        """
        assert move >= 0 and move <= 8 and move == int(move) and self.board[move] == 0
        self.playerJustMoved = 3 - self.playerJustMoved
        self.board[move] = self.playerJustMoved
        
    def GetMoves(self):
        """ Get all possible moves from this state.
        """
        return [i for i in range(9) if self.board[i] == 0]
    
    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm. 
        """
        for (x,y,z) in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
            if self.board[x] == self.board[y] == self.board[z]:
                if self.board[x] == playerjm:
                    return 1.0
                else:
                    return 0.0
        if self.GetMoves() == []: return 0.5 # draw
        assert False # Should not be possible to get here

    def __repr__(self):
        s= ""
        for i in range(9): 
            s += ".XO"[self.board[i]]
            if i % 3 == 2: s += "\n"
        return s

class state():
    def __init__(self,name,actions):
        self.name = name
        self.actions = actions

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

#construct nuclear scenario
s0 = state("s0",[])
s1 = state("s1",[])
s2 = state("s2",[])
s3 = state("s3",[])
s4 = state("s4",[])
s5 = state("s5",[])
s6 = state("s6",[])

a0 = action("a0", [s2,s6], [0.4,0.6], [-5,-1000])
a1 = action("a1", [s1,s6], [0.9,0.1], [-20,-1000])
a2 = action("a2", [s5,s6], [0.1,0.9], [100,-1000])
a3 = action("a3", [s3,s6], [0.7,0.3], [-5,-1000])
a4 = action("a4", [s5,s6], [0.3,0.7], [100,-1000])
a5 = action("a5", [s2,s6], [0.6,0.4], [-5,-1000])
a6 = action("a6", [s3,s6], [0.6,0.4], [-5,-1000])
a7 = action("a7", [s4,s6], [0.9,0.1], [-3,-1000])
a8 = action("a8", [s5,s6], [0.8,0.2], [80,-1000])
a9 = action("a9", [s5,s6], [0.2,0.8], [100,-1000])

s0.actions = [a0,a1]
s1.actions = [a2,a3]
s2.actions = [a6,a7]
s3.actions = [a4,a5]
s4.actions = [a8,a9]
#s5.actions = []	This is the goal state
#s6.actions = []	This is the fail state

#return a random state based on the probabilties of the actions outcoems
def getOutcome(a):
	r = random.randint(0,999)	
	print r	
	distribution = []
	l = 0	#lower bound
	t = 0	#cumulative probability
	for p in a.probs:
		distribution.append([l, (t+p)*1000]) #this list is the lower and upper bounds in the distribution
		l = (p*1000)
		t = t+p

	for i in range(len(a.outcomes)):
		if(r>distribution[i][0] and r<=distribution[i][1]):
			return a.outcomes[i]


#new state with uncertainty
class nuclearState():
    """
    This state models a simple mobile robot moving toward a goal state
    There are a set of motion paths which can be taken to move toward the goal state, each with different probabilities
    of success (which means there is uncertainty about the outcomes)
    """ 
    def __init__(self):
        self.currentState = s0
        
    def Clone(self):
		st = nuclearState()
		st.currentState

    #take the action
    def DoMove(self, action):
        self.currentState = getOutcome(action)

	#return list of available actions
	def GetMoves(self):
		return self.currentState.actions

	#return immediate reward (adjusted for probability)
	def GetResult():
		return = 1
		

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
        self.wins = 0
        self.visits = 0
    
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        
        #NOTE: as mentioned above, we are unable to alter the e/e bias without adding a constant UCTK (reffered to in the paper as Cp where Cp>0.
            
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
    
        return s
    
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

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
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves) 
            state.DoMove(m)
            node = node.AddChild(m,state) # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if (verbose): print rootnode.TreeToString(0)
    else: print rootnode.ChildrenToString()

    #return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
    actionlist = sorted(rootnode.childNodes, key = lambda c: c.visits, reverse=True)
    #Note, the list is generally sorted ascending and the last action taken, we sort descending and take the first

    #create a list of assessed actions from the list of nodes and remove actions with utility below the threshold
    aalist = []
    x0 = AssessedAction(actionlist[0].move, actionlist[0].visits, 0) #0 for risk because we dont have a value yet
    aalist.append(x0)
    for x in actionlist[1:]:    
        if(x.visits > (x0.utility - (x0.utility * T))):     #node utility passes threshold, make an AA
            xi = AssessedAction(x.move, x.visits, 0)
            aalist.append(xi)
    
    return aalist
           
#This method will for now substitute the BDI agent, as it is what is calling the planner
def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number 
        of UCT iterations (= simulations = tree nodes).
    """
    # state = OthelloState(4) # uncomment to play Othello on a square board of the given size
    state = OXOState() # uncomment to play OXO
    #state = NimState(15) # uncomment to play Nim with the given number of starting chips

    AAList = []

    while (state.GetMoves() != []):
        print str(state)
        if state.playerJustMoved == 1:
            AAList = UCT(rootstate = state, itermax = 1000, verbose = True) # play with values for itermax and verbose = True
        else:
            AAList = UCT(rootstate = state, itermax = 100, verbose = True)
        #print "Best Move: " + str(m) + "\n"

        #print the list of moves and associated utilities (here the utilities are simply visits, I'm not sure if this is the correct measure)
        PrintAAList(AAList)
      

        #pick a move from the list (just use the best by utility for now, this decision will ultimately be made by the BDI agent step by step and the agent will also execute the actions, but this is just to keep the program running) 
        m = AAList[0].action

        state.DoMove(m)
        raw_input()

    if state.GetResult(state.playerJustMoved) == 1.0:
        print "Player " + str(state.playerJustMoved) + " wins!"
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print "Player " + str(3 - state.playerJustMoved) + " wins!"
    else: print "Nobody wins!"

#print out an assessed action list in a nice format
def PrintAAList(l):
    for x in l:
        print "Action: "+str(x.action)+"\tUtility: "+str(x.utility)+"\tRisk: NYI"


if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players. 
    """
    #UCTPlayGame()

    print "Set the state and then call UCT"
    print "UCT(rootstate = state, itermax = [horizon])"

            
                          
            

