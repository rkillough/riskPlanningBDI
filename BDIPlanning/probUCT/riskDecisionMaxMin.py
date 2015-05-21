from __future__ import division
import math
import random


#The list will be ranked by utility, but there could be actions in the list which have both lower utiltiy and higher risk than their predecessor. These actions are obviously not desirable, so remove them.
#This satisfies the postulate: "We are only interested in actions with lower utilties if they also have lower risk"
def removeRedundantActions(aList):

    i = 1
    for x in range(len(aList) -1):
        #print i
        if(aList[i].risk > aList[i-1].risk):
            #print "Removing "+aList[i].action.name + " from options as it has higher risk than a better option"
            aList.remove(aList[i])
            i -= 1      #we've just removed an item, so set the index back to scan the next item
        i += 1
    return aList


#pick an action form alist using the max min deviation approach
def pickAction(aList, R):

	aList = removeRedundantActions(aList)

	#R is a number in sigma (standard deviations). 0 represents total risk tolerance. 

	#sortedList = sorted(aList, key=lambda action: action.utility - (R * (math.sqrt(action.risk))), reverse=True)
	sortedList = sorted(aList, key=lambda node: (node.utility/node.visits) - (R * (math.sqrt(node.risk))), reverse=True)	

	#print "\n\n"
	#for a in sortedList:
		#print str(a) + " lbound:" +  str((a.utility/a.visits) - (R* math.sqrt(a.risk)))	#recalcuated here for display, this is already done in the sort lambda

	#print "Best Action = "+str(sortedList[0])
	return sortedList[0] #return the best action

