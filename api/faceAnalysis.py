#libraries
#to analyze face
from deepface import DeepFace
import numpy
import cv2

def analyze_face(input):
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False)
    #list = [face_analysis['dominant_emotion'], face_analysis['age'], face_analysis['dominant_race']]
    return Convert(face_analysis)

def Convert(list):
    list = iter(list)
    res_dct = dict(zip(list, list))
    return res_dct