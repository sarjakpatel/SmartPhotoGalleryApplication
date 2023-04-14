#libraries
#to analyze face
from deepface import DeepFace

def analyze_face(input):
    face_analysis = DeepFace.analyze(img_path = input, enforce_detection=False)
    print(face_analysis)
    return face_analysis['dominant_race'], face_analysis['dominant_emotion'], face_analysis['age']