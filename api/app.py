#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240

# import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
from werkzeug.utils import secure_filename
import os  
import json
from flask import Flask, render_template, request
from ocr_core import ocr_core
from flask_cors import CORS
from functools import wraps

#from face_encodings import search_similar_image, store_encodings, check_face_encodings
from data import check_encodings, search_similar_image

import cv2
import numpy

app = Flask(__name__)

firebase_admin.delete_app(firebase_admin.get_app())

cred = credentials.Certificate('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbAdminConfig.json')
default_app = firebase_admin.initialize_app(cred)


app=Flask(__name__)
cred = credentials.Certificate("/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbAdminConfig.json")
# default_app=firebase_admin.initialize_app(cred)
CORS(app)
db = firestore.client()
todo_ref=db.collection('todos')  #sample collections
pb = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))

db_connect = firestore.client()
todo_ref = db_connect.collection('todos')  #sample collections ##############

firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))

@app.route("/")  #basic api
def home():
    return "hello all"

@app.route('/signup',methods=['POST'])
#@app.route('/signup',methods=['POST'])   #signup api
def signup():
    email=request.json['email']    #get the email from json
    password=request.json['password'] #get the password from json
    if email is None or password is None:
       return jsonify({'message':'username and password must not in blank'}),400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        user = pb.auth().sign_in_with_email_and_password(email, password)
        pb.auth().send_email_verification(user['idToken']) 
        return jsonify({'idToken': user['idToken'], 'message': f'Successfully created user and send verification link please activate your account '}),200
    except:
        if email:
            emailexists=auth.get_user_by_email(email)
            if(emailexists.uid):
                return jsonify({'message': 'user already exists '}),400
        else:
            return jsonify({'message': 'error creating in user'}),401

@app.route('/login',methods=['POST'])
#@app.route('/signin',methods=['POST'])  #signin api
def signin():
    email=request.json['email'] 
    password=request.json['password']
    if email is None or password is None:
        return jsonify({'message':'username and password must not to be empty'}),400
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        print(user)
        arr=''
       
        for x in user:
            if x == 'localId':
                arr=(user[x])
                
        user1= auth.get_user(arr)
        user3=user1.email_verified
        print(user3)
        if user3:
            return user
        else:
            return jsonify({'message':'please verify your account with your mailId'}),401
    except:
        return jsonify({'message':'invalid crendentails or user does not exist'}),403

'''
#logout api

@app.route("/logout")

def logout():
    #remove the token setting the user to None
    session.pop('username')
    return redirect("/login")

'''


#to protect routes

def isAuthenticated(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
      #check for the variable that pyrebase creates
      if not firebase.auth() != None:
          return redirect('/login')
      return f(*args, **kwargs)
  return decorated_function
    
  

#compute and store encodings to firebase

@app.route('/store-encodings', methods = ['POST'])
@isAuthenticated

def store_encodings1():

    email = request.json['email'] 
    image_url = request.json['image_url']

    if email is None and image_url is None:
        return jsonify({'message': 'email and image_url must not to be empty'}), 400
    
    elif email is None:
        return jsonify({'message': 'email must not to be empty'}), 400
    
    elif image_url is None:
        return jsonify({'message': 'enter image_url'}), 400
    
    #is_encoding_stored = store_encodings(email, image_url)

    elif email and image_url:

        is_encoding_stored = check_encodings(email, image_url)

        if is_encoding_stored:
            return jsonify({'message': 'stored encodings'}), 200
        
        else:
            return jsonify({'message': 'no encodings found in the image'}), 204


@app.route('/image-search', methods = ['POST'])
@isAuthenticated

def search_similar_image1():

    email = request.json['email'] 
    #email = 'rajvi.shah@sjsu.edu'
    #file = request.files['file']
    img_matrix = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    if email is None and img_matrix is None:
        return jsonify({'message': 'email must not to be empty and upload file'}), 400
    
    elif email is None:
        return jsonify({'message': 'email must not to be empty'}), 400
    
    elif img_matrix is None:
        return jsonify({'message': 'upload file'}), 400

    elif email and img_matrix:
        output_urls, keys, match1 = search_similar_image(email, img_matrix)
        

        return jsonify({'list of similar images': output_urls}), 200
    

###########################################################################

@app.route('/ocr', methods = ['POST'])
# TODO add @isAuthenticated
# TODO integrate with react app
def get_text():

    if 'file' not in request.files:
        return jsonify({'message': 'Please upload file'}), 400
    img_file = request.files['file']
    if img_file is None:
        return jsonify({'message': 'Please upload file'}), 400
    img_text = ocr_core(filename=img_file)
    return jsonify({'ocr_text':img_text}), 200
    

##########################################################################


if __name__ == '__main__':
    app.run(debug=True)

