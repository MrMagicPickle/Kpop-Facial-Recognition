from tkinter import *
from predictPage import *

class StartPage(Frame):
    
    def __init__(self, parent):
        parent.config(bg="deep sky blue")
        super().__init__()
        #main = Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)

        #top --
        #top = Frame(master=main)
        top = Frame(master=self, name="topFrame")
        top.grid(row=0, column=0, sticky="we")

        appTitle = Label(top, text="Kpop Idols Facial Recognizer", bg="deep sky blue")
        appTitle.config(font=("Arial", 40), foreground="white")
        appTitle.pack(fill="both")

        bottom = Frame(master=self, bg="deep sky blue")
        bottom.grid(row=1, column=0, sticky="nswe")
        bottom.grid_columnconfigure(0, weight=1)
        
        blankSpace = Frame(bottom, width=600, height=300, bg="deep sky blue")
        blankSpace.grid(row=0, column=0)

        menuFrame = Frame(bottom, width=600, height=300, bg="deep sky blue")
        menuFrame.grid(row=1, column=0)

        
        #-- predict button.
        predictBtn = Button(menuFrame, text="Identify Face", bg = "deep sky blue", command = lambda: parent.switchFrame(PredictPage), foreground="white", relief="ridge", font=("Helvetica", 20))
        predictBtn.grid(row=0, column=0, pady=(0,50), ipady=10)
        
        trainBtn = Button(menuFrame, text="Train Face", bg="deep sky blue", command = trainFace, foreground="white", relief="ridge", font=("Helvetica", 20))
        trainBtn.grid(row=1, column=0, ipady=10)
        

def trainFace():
    print("Training face")
