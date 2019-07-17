from tkinter import *
from inputFacePage import *
import sys
import os

sys.path.append(os.path.abspath(".."))
from globals import *


sys.path.append("C:/Users/User-HP/Desktop/My Projects/Facial Recognition/v2-0/model")
from frModel import *


class PredictPage(Frame):
    def __init__(self, parent):
        parent.config(bg="deep sky blue")
        super().__init__()
        self.grid_columnconfigure(0,weight=1)

        top = Frame(master=self, name="topFrame")
        top.grid(row=0, column=0, sticky="we")

        pageTitle = Label(top, text="Choose a Kpop group", bg="deep sky blue")
        pageTitle.config(font=("Arial", 40), foreground="white")
        pageTitle.pack(fill="both")

        bottom = Frame(master=self, name="bottomFrame", bg="deep sky blue" )

        bottom.grid(row=1, column=0, sticky="we")
        bottom.grid_columnconfigure(0, weight=1)

            
        blankSpace = Frame(bottom, bg="deep sky blue", width=1000, height=300)
        blankSpace.grid(row=0, column=0, sticky="we")
        

        optionsFrame = Frame(bottom, bg="deep sky blue", width=1000, height=300)
        optionsFrame.grid(row=0, column=0)
        
        TwiceBtn = Button(optionsFrame, text="TWICE", bg="deep sky blue", command=lambda: selectTwice(parent), foreground="white", relief="ridge", font=("Helvetica", 20))
        TwiceBtn.grid(row=0, column=0, pady=(0,50), ipady=10, padx=10)

        IzoneBtn = Button(optionsFrame, text="IZ*ONE", bg="deep sky blue", command=lambda: selectIzone(parent), foreground="white", relief="ridge", font=("Helvetica", 20))
        IzoneBtn.grid(row=0, column=1, pady=(0, 50), ipady=10, padx=10)

        WJSNBtn = Button(optionsFrame, text="WJSN", bg="deep sky blue", command=lambda: selectWJS(parent), foreground="white", relief="ridge", font=("Helvetica", 20))
        WJSNBtn.grid(row=0, column=2, pady=(0,50), ipady=10, padx=10)


        
def selectTwice(root):
    print("Selected Twice")
    #init our twice facial recognition model.
    kpopModels.twiceFRModel = FRModel(TWICE_DIR)
    kpopModels.select("twice")
    root.switchFrame(InputFacePage)
    
def selectIzone(root):
    print("Selected Izone")
    #init our Izone facial recognition model.
    kpopModels.izoneFRModel = FRModel(IZONE_DIR)
    kpopModels.select("izone")
    root.switchFrame(InputFacePage)

    
def selectWJSN(root):
    print("Selected WJSN")
    #init our wjsn facial recognition model.
    kpopModels.wjsnFRModel = FRModel(WJSN_DIR)
    kpopModels.select("wjsn")
    root.switchFrame(InputFacePage)
    
