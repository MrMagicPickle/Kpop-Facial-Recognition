import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *
import cv2
import numpy as np
from keras import backend as K
from keras.models import load_model
import keras.losses
import os
import sys

sys.path.append(os.path.abspath(".."))
from globals import *

#our loss function passed as arg during model compile.
def triplet_loss(yTrue, yPred, alpha=0.3):
    anchor, positive, negative = yPred[0], yPred[1], yPred[2]

    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,
               positive)), axis=-1)
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, 
               negative)), axis=-1)
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
   
    return loss









class FRModel():
    def __init__(self, kpopGroupDir):

        K.set_image_data_format('channels_first')
        print("loading model")


        self.FRmodel = load_model(FACE_RECO_MODEL_WITH_WEIGHTS, custom_objects= {'triplet_loss': triplet_loss})
        print("Model finished loading")
        self.db = {}
        self.kpopGroupDir = kpopGroupDir
        self.prepareDB()

    def prepareDB(self):

        for root, dirs, files in os.walk(self.kpopGroupDir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()
                    idolNameDirPath = os.path.dirname(path)
                    identity = os.path.basename(idolNameDirPath)                
                    print("Training: " + identity + " --path: " + path)

                    #center the face.
                    face = self.getFace(path)
                    if dbg_train_displayImg:
                        cv2.imshow("Trained image face detected", face)
                        cv2.waitKey(0)
                    #TODO: we might want to accumulate the encodings of multiple pictures
                    if not identity in self.db:                
                        self.db[identity] = [img_to_encoding(face, self.FRmodel)]
                    else:
                        self.db[identity].append(img_to_encoding(face, self.FRmodel))

        #iterate through each value (list) of each key and calculate the average encoding value.
        for (id, encList) in self.db.items():
            meanEnc = encList[0]
            if len(encList) <= 1:
                self.db[id] = meanEnc
                continue
        
            for  i in range (1, len(encList)):
                meanEnc += encList[i]
            meanEnc = meanEnc / len(encList)
            
            self.db[id] = meanEnc

            
        self.saveDB(self.db, "kpopModel.csv")
        return self.db

    def saveDB(self, db, filePath):
        dbFile = open(filePath, 'w')
        for (id, enc) in db.items():
            dbFile.write(id + " " )
            for k in range (len(enc[0])):
                dbFile.write(str(enc[0][k]) + " ")
            
            dbFile.write("\n")
        dbFile.close()
    

    def predict(self, imgPath):
        face = self.getFace(imgPath)
        if face is None:
            print("No face detected in this image")
            return None

        if dbg_predict_displayImg:
            cv2.imshow("Predict face detected", face)
            cv2.waitKey(0)
        encoding = img_to_encoding(face, self.FRmodel)
    
        min_dist = 100
        identity = None
        
        # Loop over the self.db dictionary's names and encodings.
        for (name, db_enc) in self.db.items():
            dist = np.linalg.norm(db_enc - encoding)
            if dbg_face_dist_val:
                print('distance for %s is %s' %(name, dist))
            if dist < min_dist:
                min_dist = dist
                identity = name
    
        if min_dist > 0.52:
            return None
        else:
            return identity
        

        
        
    def getFace(self, imgPath):
        roiImg = None
        img = cv2.imread(imgPath)
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

        faces = faceDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            return None
    
        print(str(len(faces)) + " --path: "  + imgPath)
        x, y, w, h = self.getLargestFace(faces, img)

    
        roiGray = gray[y:y+h, x:x+w]
        grayCopy = gray.copy()
        cv2.rectangle(grayCopy, (x, y), (x+w, y+h), (255,0,0), 1)
        if dbg_getFace_displayImg:
            cv2.imshow("get face of prediction", grayCopy)
            cv2.waitKey(0)
            
        roiImg = img[y:y+h, x:x+w]
        return roiImg

    def getLargestFace(self,faces, img):
        largestArea = 0
        largestFace = None
        for (x, y, w, h) in faces:
            roi = img[y:y+h, x:x+w]
            height, width = roi.shape[:2]
            area = height * width
            if area > largestArea:
                largestArea = area
                largestFace = (x, y, w, h)
        return largestFace
    
