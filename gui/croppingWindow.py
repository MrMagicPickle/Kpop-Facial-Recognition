from tkinter import *
import PIL.Image
import PIL.ImageTk


import sys
import os
sys.path.append(os.path.abspath(".."))
from globals import *



class DrawableWindow(Toplevel):
    def __init__(self, parent, callback, myCursor=None):
        super().__init__(parent)
        self.config(cursor=myCursor)

        #our image.
        self.loadedImg = None

        #load image.
        self.loadImage(SSPATH)


        #init our canvas. - make it match the size of our image.
        self.canvas = Canvas(self, width=self.loadedImg.width(), height=self.loadedImg.height(), name="newWindowCanvas")
        self.canvas.pack()

        #draw the image onto our canvas.
        self.canvas.create_image(0,0, image=self.loadedImg, anchor="nw")
        #need to keep reference because of shitty python garbage disposal.
        #..Image wont load if you dont keep a reference.
        self.canvas.image = self.loadedImg


        
        self.bind('<Button-1>', self.btnOneClicked)
        self.bind('<ButtonRelease-1>', self.btnOneReleased)
        self.bind('<B1-Motion>', self.btnOneMotion)
        self.bind('<Escape>', exitApp)

        #mouse positions.
        self.startPos = None
        self.currPos = None
        self.endPos = None


        #our cropping rectangle.
        self.rect = None

        #callback function.
        self.callback = callback

        

        
    def btnOneClicked(self, event):
        print("Button one clicked")
        print(self.loadedImg)
        self.startPos = [event.x, event.y]
        #store the starting position.
        if not self.rect is None:
            self.canvas.delete(self.rect)
            
        self.rect = self.canvas.create_rectangle(self.startPos[0], self.startPos[1], self.startPos[0], self.startPos[1], outline="red")
            

    def btnOneReleased(self, event):
        print("Button one released")
        #store the ending position.
        self.endPos = [event.x, event.y]
        if self.endPos[0]- self.startPos[0] <= 0:
            return

        if self.endPos[1] - self.startPos[1] <= 0:
            return
        
        #- crop ROI rect and write it to folder.
        #TODO: Find a way to crop the image without having to re-open it with Pillow.
        img = PIL.Image.open(SSPATH)
        roi = (self.startPos[0], self.startPos[1], self.endPos[0], self.endPos[1])
        img = img.crop(roi)
        img.save(CROP_IMG_PATH, "PNG")

        #- send it for reading.
        self.callback(img)
      
        #destroy the window.
        self.destroy()






    def btnOneMotion(self, event):
        self.currPos = [event.x, event.y]

        self.canvas.coords(self.rect, self.startPos[0], self.startPos[1], self.currPos[0], self.currPos[1])

    def loadImage(self, imgPath):
        img = PIL.Image.open(imgPath)
        photo = PIL.ImageTk.PhotoImage(img)
        self.loadedImg = photo

        
def exitApp(event):
    self.destroy()
