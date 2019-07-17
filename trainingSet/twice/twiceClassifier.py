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

sys.path.append(os.path.abspath("../.."))
from globals import *



faceDetector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)


class TwiceFRModel():
    def __init__(self, trainImgDir):
        
        K.set_image_data_format('channels_first')
        print("loading model")


        self.FRmodel = load_model("FaceRecoModelWithWeights.h5", custom_objects= {'triplet_loss': triplet_loss})
        print("Model finished loading")
        self.db = {}
        self.trainImgDir = trainImgDir

    def prepareDB(self):

        for root, dirs, files in os.walk(self.trainImgDir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ", "-").lower()
                    idolNameDirPath = os.path.dirname(path)
                    identity = os.path.basename(idolNameDirPath)                
                    print("Training: " + identity + " --path: " + path)

                    #center the face.
                    face = getFace(path)

                    #TODO: we might want to accumulate the encodings of multiple pictures
                    if not identity in self.db:                
                        self.db[identity] = [img_to_encoding(face, FRmodel)]
                    else:
                        self.db[identity].append(img_to_encoding(face, FRmodel))

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

        return self.db

    def predict(self, imgPath):
        encoding = img_to_encoding(imgPath, self.model)
    
        min_dist = 100
        identity = None
        
        # Loop over the self.db dictionary's names and encodings.
        for (name, db_enc) in self.db.items():
            dist = np.linalg.norm(db_enc - encoding)
            print('distance for %s is %s' %(name, dist))
            if dist < min_dist:
                min_dist = dist
                identity = name
    
        if min_dist > 0.52:
            return None
        else:
            return identity
        

        
        
