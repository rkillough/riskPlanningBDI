

from Tkinter import *
import riskDecisionSD
import riskDecision



def switchStrategy():
    global strategy
    global slabel 
    print "Clicked"
    alistbox.delete(1.0,7.13)
    if(strategy == riskDecision):
        strategy = riskDecisionSD
        slabel.config(text = "Strategy:Confidence")
        alistbox.insert(INSERT, makeActionString())
    else:
        strategy = riskDecision    
        slabel.config(text = "Strategy:Ratio")
        alistbox.insert(INSERT, makeActionString())

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

def makeActionString():
	aList = strategy.getActions()
	string = ""
	for a in aList:
		string += '('+a.name+','+str(a.utility)+','+str(a.risk)+')\n'
	return string

top = Tk()

top.minsize(width=400, height= 550)


strategy = riskDecisionSD

alistbox = Text(top, padx=5, pady=5, height=20, width=20)
#alistbox.insert(INSERT, "(a0, 40, 450)\n(a1, 20, 200)\n(a2, 19, 170)\n(a3, 15,  99)\n(a4,  0,   0)\n(a5, -20, 48)\n(a6, -22,  0)")
alistbox.insert(INSERT, makeActionString())
alistbox.place(anchor=NW)

#changeSelect(1)
#alistbox.tag_config("sel", background="yellow")

slabel = Label(top, text="Strategy:Confidence")
slabel.pack(anchor=NE)
button = Button(top, command=switchStrategy, text="Switch Strategy")
button.pack(anchor=NE)

val = DoubleVar()
slider = Scale(top, orient=VERTICAL, length=500, from_=1, to=0, resolution=0.01, command=slide)
slider.pack(anchor=SE)

label = Label(top, text="")
label.pack(anchor=NE)



top.mainloop()
