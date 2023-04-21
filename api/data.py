#libraries
#to compute encodings
import cv2
import face_recognition
from PIL import Image
from fer import FER
from deepface import DeepFace
import requests
import numpy
import PIL
#to store encodings
import firebase_admin
from firebase_admin import credentials, firestore
import numpy
import json
import pyrebase
import base64
import os
import io

cred_file_path = "/home/vishnu-yeruva/Documents/Edu/CMPE295B/Project/SmartPhotoGalleryApplication/api/fbAdminConfig.json"
cred = credentials.Certificate(cred_file_path)
firebase_admin.initialize_app(cred)

# this connects to our Firestore database
db = firestore.client() 

firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE295B/Project/SmartPhotoGalleryApplication/api/fbconfig.json')))
storage = firebase.storage()

#cascade_file_path = "C:/Users/HP/Downloads/data/haarcascades/haarcascade_frontalface_alt2.xml"
cascade_file_path = r"cascades/data/haarcascades/haarcascade_frontalface_alt2.xml"
face_cascade = cv2.CascadeClassifier(cascade_file_path)

def compute_face_encodings(input):

    if isinstance(input, str):

        img = Image.open(requests.get(input, stream=True).raw)

        img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    
    else:

        #file_name_string = base64.urlsafe_b64encode(url)
        #pil_image = PIL.Image.open(input)
        img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
        #img = cv2.imread(input)
        # img = input
    
    #img = cv2.imread(opencvImage)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 0)

    #print(len(faces))
    
    print('Number of faces detected:', len(faces))

    if len(faces)>0:
        
        
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)

        print('Computed encodings')
    
        return encoding
    
    else:
        
        return []#returns ndarray


def store_cropped_image(email, image_url, token):

    img_format = Image.open(requests.get(image_url, stream=True).raw)
    
    img = cv2.cvtColor(numpy.array(img_format), cv2.COLOR_RGB2BGR)
    

    #img = cv2.imread(opencvImage)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    #print(faces)

    #print(len(faces))

    if (len(faces) > 0):
        urls = []
        keys = []
        #print(i_val)
        for i in range(len(faces)):
            
            (x, y, w, h) = faces[i]
            

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 0)
        

            #boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
            boxes = [(y, x + w, y + h, x)]
            face_encoding = face_recognition.face_encodings(rgb, boxes)
            
            face = img[y:y + h, x:x + w]

            url_ref = db.collection("userDetails").document(email).collection("data")
            # Add documents to the subcollection.
            url1_ref = url_ref.document("cropped_face_url")
            prev_stored_urls = url1_ref.get().to_dict()

            url_ref = db.collection("userDetails").document(email).collection("data")
            encodings_ref = url_ref.document("face_encodings")
            prev_stored_encodings = encodings_ref.get().to_dict()

            url_ref = db.collection("userDetails").document(email).collection("data")
            image_urls_ref = url_ref.document("image_urls")
            prev_stored_image_urls = image_urls_ref.get().to_dict()
            

            if prev_stored_urls:
                length = len(prev_stored_urls)

            else:
                length = 0
            
            file_path = email + "_face_" + str(length) + ".jpg"
            ####################
            cv2.imwrite(file_path, face)

            res = storage.child(file_path).put(file_path)

            # Get url of image
            url = storage.child(file_path).get_url(token)
            urls.append(url)

            #store face url to firebase db
            if prev_stored_urls:
                length = len(prev_stored_urls)
                key = str(length)
                url1_ref.update({key : url})
                keys.append(key)
                face_encoding = numpy.array(face_encoding)
                face_encoding = numpy.array2string(face_encoding, separator=',', suppress_small = True)
                encodings_ref.update({key: face_encoding})

                image_urls_ref.update({key: [image_url]})
            
                print('Added face url to the firebase db')
                #return 'done'

        
            #when the first encoding is stored in a user's account
            else:
                
                key = '0'
                url1_ref.set({key : url})
                keys.append(key)
                face_encoding = numpy.array(face_encoding)
                face_encoding = numpy.array2string(face_encoding, separator=',', suppress_small = True)
                encodings_ref.set({key: face_encoding})

                image_urls_ref.set({key: [image_url]})
                print('Added first face url to the firebase db')
                #return 'done'
                        
        return urls, keys
        
    else:
        
        #no faces encoded
        return [], []


def search_similar_image(email, image_url):

    faces = compute_face_encodings(image_url)
    flag = 0
    if len(faces)>0:
        
        flag = 1
        print('Computed face encodings for a given image url')
        faces1 = len(faces)

        doc_ref = db.collection("userDetails").document(email).collection("data")
        print('Database connected')
        encoding_ref = doc_ref.document("face_encodings")
        stored_encodings = encoding_ref.get().to_dict()

        doc_ref = db.collection("userDetails").document(email).collection("data")
        url_ref = doc_ref.document("image_urls")
        stored_urls = url_ref.get().to_dict()

        dict_of_encodings = {}
        
    
        output_urls = []

        if stored_encodings:
            match1 = []

            for key in stored_encodings.keys():
                encoding = stored_encodings[key]
                #stored encoding type coversion
                encoding = encoding.replace('[', '').replace(']', '').replace('\n', '')
                new_encoding = list(encoding.split(","))
                new_encoding1 = [eval(i) for i in new_encoding]
                dict_of_encodings.update({key : new_encoding1})
            print('Collected all encodings from the firebase')
            #print(dict_of_encodings)
            
            keys = []
        
            for face_encoding1 in faces:
                i = 0
                for key in dict_of_encodings.keys():
                    
                    face_encoding2 = dict_of_encodings[key]


                    face_encoding1 = numpy.array(face_encoding1)
                    face_encoding2 = numpy.array(face_encoding2)

                    matches = face_recognition.compare_faces([face_encoding1], face_encoding2, tolerance = 0.5)
                    is_match = any(matches)
                    
                    print('Are faces matching:', is_match)

                    if is_match:
                        current_url = stored_urls[key]
                        output_urls.append(current_url)
                        keys.append(key)
                        match1 = True
                    
            return output_urls, keys, match1, flag
        
        else:
            return output_urls, None, False, flag
    else:
        #no encodings found
        return [], [], False, flag



def check_encodings(email, image_url, token):

    urls, keys, is_match, flag = search_similar_image(email, image_url)
    if flag == 0:
        return False
    
    else:

        print('Face matched?', is_match)
        
        doc_ref = db.collection("userDetails").document(email).collection("data")
        print('Database connected')

        url_ref = doc_ref.document("image_urls")
        stored_urls = url_ref.get().to_dict()
        
        
        if is_match:
                
            for key in keys:
        
                url_ref.update({key: firestore.ArrayUnion([image_url])})
            print("Given image encodings matched with the stored encodings so updated image_urls hashmap")
            
            return True

        else:

            store_cropped_image(email, image_url, token)

            return True

def deblur_image1(input_image):

    image = cv2.cvtColor(numpy.array(input_image), cv2.COLOR_RGB2BGR)
    #image = cv2.imread('input.jpg')

    kernel = numpy.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

    sharpened = cv2.filter2D(image, -1, kernel)
    print(type(sharpened))
    img = PIL.Image.fromarray(sharpened)

    data = io.BytesIO()
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    cv2.imwrite('sharpened.jpg', sharpened)
    my_str = encoded_img_data.decode('utf-8')
    return my_str
    #return 'sharpened.jpg'
    
try:  
    from PIL import Image
except ImportError:  
    import Image
import pytesseract

def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def compute_emotion(input):
    detector = FER(mtcnn=True)
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    emotion = detector.detect_emotions(img)
    print(emotion)
    dominant_emotion = detector.top_emotion(img)
    return dominant_emotion

def deblur_image1(input_image):

    image = cv2.cvtColor(numpy.array(input_image), cv2.COLOR_RGB2BGR)
    #image = cv2.imread('input.jpg')

    kernel = numpy.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

    sharpened = cv2.filter2D(image, -1, kernel)
    print(type(sharpened))
    img = PIL.Image.fromarray(sharpened)

    data = io.BytesIO()
    img.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())
    cv2.imwrite('sharpened.jpg', sharpened)
    my_str = encoded_img_data.decode('utf-8')
    return my_str
    #return 'sharpened.jpg'

def analyze_face(input):
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False)
    #list = [face_analysis['dominant_emotion'], face_analysis['age'], face_analysis['dominant_race']]
    return Convert(face_analysis)

def Convert(list):
    list = iter(list)
    res_dct = dict(zip(list, list))
    return res_dct
