

from Tkinter import *
import riskDecisionSD
import riskDecision


class AA():
	def __init__(self, a, u, r):
		self.action = a
		self.utility = u
		self.risk = r

	def __repr__():
		return "("+self.action+","+str(self.utility)+","str(self.risk)+")"

a0 = AA("a0", 10, 25)
a1 = AA("a1", 5, 9)
a2 = AA("a2", 7, 64)
a3 = AA("a3", -50, 4)


#called when slider slided
def slide(val):
	action = strategy.pickAction(float(val))
	label.config(text = "R = "+str(val))
	changeSelect(action)




#Change the currently highlighted action to indicate it is the current best
def changeSelect(val):
    val += 1
    s1 = str(val)+".0"
    s2 = str(val)+".13"
    
    alistbox.tag_remove("sel", 1.0, 7.13)

    alistbox.tag_add("sel", s1, s2)

def ChangeApproach():
	pass

top = Tk()

top.minsize(width=700, height= 550)


strategy = riskDecisionSD

alistbox = Text(top, padx=5, pady=5, height=20, width=20)


alistbox.pack(side=LEFT)









button = Button(top, command=ChangeApproach, text="ChangeApproach")
button.pack(anchor=NE)


Rslider = Scale(top, orient=VERTICAL, length=500, from_=1, to=0, resolution=0.01, command=slide)
Rslider.pack(side=LEFT)

slider1 = Scale(top, orient=VERTICAL, length=500, from_=100, to=-100, resolution=0.01, command=slide)
slider1.pack(side=RIGHT)

slider2 = Scale(top, orient=VERTICAL, length=500, from_=100, to=-100, resolution=0.01, command=slide)
slider2.pack(side=RIGHT)

slider3 = Scale(top, orient=VERTICAL, length=500, from_=100, to=-100, resolution=0.01, command=slide)
slider3.pack(side=RIGHT)

slider4 = Scale(top, orient=VERTICAL, length=500, from_=100, to=-100, resolution=0.01, command=slide)
slider4.pack(side=RIGHT)



#label = Label(top, text="")
#label.pack(anchor=NE)



top.mainloop()
