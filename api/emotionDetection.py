#libraries
#to compute emotion
from fer import FER
from fer import Video
import numpy
import cv2

def compute_emotion(input):
    detector = FER(mtcnn=True)
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    emotion = detector.detect_emotions(img)
    dominant_emotion = detector.top_emotion(img)
    return dominant_emotion
