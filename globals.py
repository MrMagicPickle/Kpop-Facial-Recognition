import cv2
import tensorflow as tf
import os

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
dbg_train_displayImg = False
dbg_predict_displayImg = False
dbg_getFace_displayImg = False
dbg_face_dist_val = True

FACE_RECO_MODEL_WITH_WEIGHTS = os.path.join(CURR_DIR, "model/FaceRecoModelWithWeights.h5")


FACE_RECO_MODEL_DIR = os.path.join(CURR_DIR, "model/")

CLASSIFIER_DIR = os.path.join(CURR_DIR, "classifier/")

FACE_DETECTOR_PATH = os.path.join(CURR_DIR, "faceDetector/haarcascade_frontalface_alt.xml")

CROP_IMG_PATH = os.path.join(CURR_DIR, "gui/screenshots/croppedFace.png")

SSPATH = os.path.join(CURR_DIR, "gui/screenshots/ss1.png")

faceDetector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)

#----- KPOP GROUP DIR -----#
TWICE_DIR = os.path.join(CURR_DIR, "trainingSet/twice/images/")
RV_DIR = os.path.join(CURR_DIR, "trainingSet/red-velvet/")
WJSN_DIR = os.path.join(CURR_DIR, "trainingSet/wjsn/")
IZONE_DIR = os.path.join(CURR_DIR, "trainingSet/izone/")
G_IDLE_DIR = os.path.join(CURR_DIR, "trainingSet/g-idle/")


class KpopModels():
    def __init__(self):
        self.twiceFRModel = None
        self.redVelvetFRModel = None
        self.izoneFRModel = None
        self.wjsnFRModel = None
        self.gIdleFRModel = None

        self.selectedModel = None

    def select(self, kpopGroupKey):
        if kpopGroupKey == "twice":
            self.selectedModel = self.twiceFRModel
        if kpopGroupKey == "izone":
            self.selectedModel = self.izoneFRModel
        if kpopGroupKey == "wjsn":
            self.selectedModel = self.wjsnFRModel
            
            

#global state for verything to access it.
kpopModels = KpopModels()
