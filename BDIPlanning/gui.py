

from Tkinter import *
 

def slide(val):
    label.config(text = str(val))

#def changeBestAction(aNumber):
    

top = Tk()

alistbox = Text(top, padx=5, pady=5, height=6, width=20)
alistbox.insert(INSERT, "(a0, 40, 450)\n(a1, 20, 200)")
alistbox.pack(anchor=NW)

alistbox.tag_add("sel", "2.0", "2.13")
alistbox.tag_config("sel", background="yellow")


val = DoubleVar()
slider = Scale(top, orient=HORIZONTAL, length=500, from_=0, to=1, resolution=0.01, command=slide)
slider.pack(anchor=SW)

label = Label(top, text="none")
label.pack(anchor=NE)

top.mainloop()
