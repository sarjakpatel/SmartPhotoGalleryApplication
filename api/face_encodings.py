#to compute encodings
import cv2
import face_recognition
from PIL import Image
import requests
import numpy

#to store encodings
import firebase_admin
from firebase_admin import credentials, firestore
import numpy
import json

#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#cascade_file_path = "C:/Users/HP/Downloads/data/haarcascades/haarcascade_frontalface_alt2.xml"
cascade_file_path = r"cascades/data/haarcascades/haarcascade_frontalface_alt2.xml"
face_cascade = cv2.CascadeClassifier(cascade_file_path)

email = 'rajvi.shah@sjsu.edu'
url = 'https://firebasestorage.googleapis.com/v0/b/user-auth-42504.appspot.com/o/IMG_20220530_092140.jpg?alt=media&token=2535b011-e8dc-45ec-a57c-4f8e70096be4'



def compute_face_encodings(url):

    img = Image.open(requests.get(url, stream=True).raw)
    
    img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    

    #img = cv2.imread(opencvImage)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)

    #print(len(faces))

    if (len(faces) == 1):
        
        
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)
    
        return encoding
    
    else:
        
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)
        
        return encoding #returns ndarray


       

#print(compute_face_encodings(url))


cred_path = "C:/Rajvi/Project/Smart Gallery Photo Application/user-authentication/fbAdminConfig.json"

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# this connects to our Firestore database
db = firestore.client()  

def store_encodings(email, image_url):
    

    encodings = compute_face_encodings(url)

    print('Computed face encodings/ Face detected in the given image url:', len(encodings))

    #to make "encodings" collection in email
    doc_ref = db.collection("userDetails").document(email).collection("data")

    # Add documents to the subcollection.
    encoding_ref = doc_ref.document("encodings")
    prev_stored_encodings = encoding_ref.get().to_dict()
    #print(type(prev_stored_encodings))
    print('Previously stored image encodings in firebase:', len(prev_stored_encodings))

    url_ref = doc_ref.document("image_urls")
    prev_stored_urls = url_ref.get().to_dict()
    print('Previously stored image urls in firebase:', len(prev_stored_urls))


    for encoding in encodings:
            
        encoding = numpy.array2string(encoding, separator=',', suppress_small = True)
        #print(encoding)
        #print(type(encoding))
        print('Converted encodings (ndarray) to str-----')

        
        if prev_stored_encodings:
            length = len(prev_stored_encodings)
            
            #if encoding already exits then add url to that encoding
            if encoding in prev_stored_encodings.items():
                
                key = str(prev_stored_encodings.items(encoding))
                value = firestore.ArrayUnion([url])
                
                url_ref.update({key: value})
                print('Updated url as current encoding already exists')
                return True
            #if new encoding then add encoding and url
            else:
                
                key = str(length)
                encoding_ref.update({key : encoding})
                url_ref.update({key : url})
                print('Added encoding and url to the firebase')
                return True

        
        #when the first encoding is stored in a user's account
        else:
            
            key = '0'
            encoding_ref.set({key : encoding})
            url_ref.set({key : url})
            print('Added first encoding and url')
            return True

    return False
            
#cred_path = "C:/Rajvi/Project/Smart Gallery Photo Application/user-authentication/fbAdminConfig.json"

cred = credentials.Certificate(fbAdminConfig.json)
firebase_admin.initialize_app(cred)

# this connects to our Firestore database
db = firestore.client()  

def search_similar_image(email, image_url):


    face_encoding1 = compute_face_encodings(image_url)
    print(type(face_encoding1))
    print('Computed face encodings for a given image url')
    
    doc_ref = db.collection("userDetails").document(email).collection("data")

    print('Database connected')
    # Add documents to the subcollection.
    encoding_ref = doc_ref.document("encodings")
    stored_encodings = encoding_ref.get().to_dict()

    url_ref = doc_ref.document("image_urls")
    stored_urls = url_ref.get().to_dict()

    list_of_encodings = []

    
    for encoding in stored_encodings.values():
        #print(encoding)
        encoding = encoding.replace('[', '').replace(']', '').replace('\n', '')
        
        new_encoding = list(encoding.split(","))
        new_encoding1 = [eval(i) for i in new_encoding]
        list_of_encodings.append(new_encoding1)

    print('Collected all encodings from the firebase')
    #print(list_of_encodings)

    list_of_urls = []
    for url in stored_urls.values():
        list_of_urls.append(url)
    print('Collected all urls from the firebase')
    
    #print(list_of_urls)

    output_urls = []
    for face_encoding2 in list_of_encodings:
        count = 0
        
        face_encoding1 = numpy.array(face_encoding1)
        face_encoding2 = numpy.array(face_encoding2)

        matches = face_recognition.compare_faces(face_encoding1, face_encoding2, tolerance = 0.5)
        is_match = any(matches)
        
        print('Are faces matching:', is_match)

        if is_match:
            current_url = list_of_urls[count]
            output_urls.append(current_url)
        
        count += 1

    return output_urls

#print(search_similar_image(email, url))

