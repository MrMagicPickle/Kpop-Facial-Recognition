from tkinter import *
import PIL.Image
import PIL.ImageTk
import pyautogui
import time
from croppingWindow import *

import sys
import os
sys.path.append(os.path.abspath(".."))
from globals import *



class InputFacePage(Frame):
    def __init__(self, parent):
        parent.config(bg="deep sky blue")
        self.parent = parent
        super().__init__()
        self.grid_columnconfigure(0, weight=1)
        
        main = Frame(master=self, name="topFrame", bg="deep sky blue")
        main.grid(row=0, column=0, sticky="we")
        main.grid_columnconfigure(0, weight=1)
        
        pageTitle = Label(main, text="Drag and drop the Kpop Idol's face", bg="deep sky blue")
        pageTitle.config(font=("Arial", 40), foreground="white")
        pageTitle.grid(row=0, column=0, pady=(0,100))

        selectFaceBtn = Button(main, text="Select Face", bg="deep sky blue", command=lambda: self.getFace(), relief="ridge", foreground="white", font=("Helvetica", 20))
        selectFaceBtn.grid(row=1, column=0, pady=(0, 40))

        self.displayImg = None

        self.canvas = Canvas(self, width=300, height=500, name="inputFaceCanvas", bg="deep sky blue", borderwidth=0, highlightthickness=0)
        #self.canvas = Canvas(self, width=300, height=500, name="inputFaceCanvas", bg="deep sky blue")
        self.canvas.grid(row=2, column=0, sticky="nswe")

    def getFace(self):
        #minimize the app.
        self.parent.iconify()

        #sleep time for a while so that we dont screenshot the app before it minimzes.
        time.sleep(0.25)
        
        print("Retrieving screenshot")
        pyautogui.screenshot(SSPATH)

    
                
        print("Building new window")
        newWin = DrawableWindow(self.parent, self.getCroppedImgHook, "cross")
        

        
    def getCroppedImgHook(self, img):
        self.parent.deiconify()
        photo = PIL.ImageTk.PhotoImage(img)
        #top coordinate.
        distFromTopToImg = self.canvas.winfo_height()/2 - photo.height()/2
        yCoord = self.canvas.winfo_height()/2 - distFromTopToImg
        self.canvas.create_image(self.canvas.winfo_width()/2, yCoord, image=photo)
        self.canvas.image = photo

        #send for face recognition.
        id = kpopModels.selectedModel.predict(CROP_IMG_PATH)
        print("Detected: " + str(id))
        

        
        

    
        
        
