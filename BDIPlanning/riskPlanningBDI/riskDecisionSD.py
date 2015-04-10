'''
The is the same a riskdivision.py except we use a differnt measure to calculate the best action, namely the percentage confidence that the outcoem wil be in a range R. Where r is simply a ration of the mean and the range is this ratio applied to the mean aroud the mean
'''

from __future__ import division
import math

cResource = 100 #this should have a negative correlation with R

class Action():
    def __init__(self, name, utility, risk):
        self.name = name
        self.utility = utility
        self.risk = risk

    def __repr__(self):
        return self.name + ", "+ str(self.utility) + ", "+ str(self.risk)
            

a0 = Action("a0", 40, 450)
a1 = Action("a1", 20, 200)
a2 = Action("a2", 19, 100)
a3 = Action("a3", 2 , 10 )

aList = [a0,a1,a2,a3]



def pickAction(R):
    print("R= "+str(R))
    
    topactionConf = 0       #the highest percentage confidence so far
    for a in aList:
        #calculate the tolerance range (just calculate the top one, doesnt matter either way)
        trange = a.utility * R
        SD = math.sqrt(a.risk)  #calc the standard deviation
        confidence = (trange / SD) * 68.27
        print "Confidence "+a.name+" is in interval is "+str(confidence)
    
    
    #print(selectedAction)
    #return selectedAction
        

def adjustRiskTolerance():
    R=1 

    for i in range(100):
        print(R)
        print(pickAction(R))
        print
        R = R - 0.01

#adjustRiskTolerance()
#print(adjustRiskTolerance())
