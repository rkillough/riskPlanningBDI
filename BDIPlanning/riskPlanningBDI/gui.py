

from Tkinter import *
import riskDecision
 
#called when slider slided
def slide(val):
   
    action = riskDecision.pickAction(float(val))
    label.config(text = "R = "+str(val))
    changeSelect(action)

#Change the currently highlighted action to indicate it is the current best
def changeSelect(val):
    val += 1
    s1 = str(val)+".0"
    s2 = str(val)+".13"
    
    alistbox.tag_remove("sel", 1.0, 4.13)

    alistbox.tag_add("sel", s1, s2)

top = Tk()

alistbox = Text(top, padx=5, pady=5, height=6, width=20)
alistbox.insert(INSERT, "(a0, 40, 450)\n(a1, 20, 200)\n(a2, 19, 100)\n(a3,  2,  10)")
alistbox.pack(anchor=NW)

#changeSelect(1)
#alistbox.tag_config("sel", background="yellow")


val = DoubleVar()
slider = Scale(top, orient=HORIZONTAL, length=500, from_=0, to=1, resolution=0.001, command=slide)
slider.pack(anchor=SW)

label = Label(top, text="none")
label.pack(anchor=NE)

top.mainloop()
