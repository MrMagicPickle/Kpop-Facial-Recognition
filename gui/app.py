from tkinter import *
from startPage import *



class KpopFaceRecognitionApp(Tk):    
    def __init__(self):
        Tk.__init__(self)
        self.geometry("1200x800")
        self.bind('<Escape>', self.exitApp)
        self.grid_columnconfigure(0, weight=1)
        
        self._frame = None
        self.switchFrame(StartPage)

    def switchFrame(self, frameClass):
        newFrame = frameClass(self)
        

        if self._frame is not None:
            self._frame.destroy()
        self._frame = newFrame
        self._frame.grid(row=0, column=0, sticky="nswe")
        
   
    def exitApp(self, event):
        self.destroy()
        
        

def predictFace():
    print("To the Predict face page!")
    

    
def printChildren(parent):
    for i in range (len(parent.winfo_children())):
        print(str(parent.winfo_children()[i]))



            
testVal = "4123123"        
