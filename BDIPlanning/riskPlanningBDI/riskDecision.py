

R = 1
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

#pick an action by comparing the ratio of the loss of utility to the ratio of the reduction in risk
#This comparison is adjusted by the constant R
def pickAction():
	selectedAction = aList[0] 	#first action selectedd by default
	for i in range(len(aList)-1):
		uRatio = (aList[i].utility-aList[i+1].utility) / aList[i].utility
		#print(uRatio)
		rRatio = (aList[i].risk-aList[i+1].risk) / aList[i].risk
		#print("Ratio: "+ aList[i].name +": "+ str(uRatio) +", "+ str(rRatio))
		if(rRatio * R > uRatio):
			selectedAction = aList[i+1]
		else:
			return selectedAction
		
	return selectedAction
		

def adjustRiskTolerance():
	global R

	for i in range(100):
		print(R)
		print(pickAction())
		print
		R = R - 0.01

#adjustRiskTolerance()
print(adjustRiskTolerance())
