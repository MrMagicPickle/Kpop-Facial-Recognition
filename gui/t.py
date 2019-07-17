import sys
import os

sys.path.append(os.path.abspath(".."))
from globals import *

sys.path.append('C:/Users/User-HP/Desktop/My Projects/Facial Recognition/v2-0/model')
from frModel import *

def main():
    fr = FRModel(TWICE_DIR)

