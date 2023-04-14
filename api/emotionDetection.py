#libraries
#to compute emotion
from fer import FER
from fer import Video
import cv2

def compute_emotion(input):
    detector = FER(mtcnn=True)
    img = cv2.imread(input)
    emotion = detector.detect_emotions(img)
    dominant_emotion = detector.top_emotion(img)
    print(emotion)
    
    if input.endswith('.mp4'):
        video = Video(input)
        raw_data = video.analyze(detector, display=True)
        df = video.to_pandas(raw_data)
        print(df)
    
    return dominant_emotion
