from __future__ import division
import math
import random

aList = []

class Action():
	def __init__(self, name, utility, risk):
		self.name = name
		self.utility = utility
		self.risk = risk
	def __repr__(self):
		return self.name + ", "+ str(self.utility) + ", "+ str(self.risk)

#Generate a set of 5 random actions within the constraint rules
def generateActions():
	global aList
	aList = []
	for i in range(5):
		if(i == 0):
			aList.append(Action("a0", random.randint(-999,999), random.randint(0,9999)))
		else:
			aList.append(Action("a"+str(i), random.randint(-999,aList[i-1].utility-1), random.randint(0,aList[i-1].risk-1)))

#pick an action form alist using the max min deviation approach
def pickAction(R):

	#R is a number in sigma (standard deviations). 0 represents total risk tolerance. 

	sortedList = sorted(aList, key=lambda action: action.utility - (R * (math.sqrt(action.risk))), reverse=True)

	#for a in sortedList:
		#print str(a) + "\t\t lbound:" +  str(a.utility - (R* math.sqrt(a.risk)))	#recalcuated here for display, this is already done in the sort lambda

	#print "Best Action = "+str(sortList[0])
	return sortedList[0] #return the best action

def testrun():

	generateActions()

	for a in aList:
		print a

	print "\n\n"

	currentBest = Action("none",0,0)
	for i in range(1000):
		a = pickAction(i)
		if(a.name != currentBest.name):
			print "Best action @ "+str(i) + " is " + str(a)
			currentBest = a
	
testrun()
