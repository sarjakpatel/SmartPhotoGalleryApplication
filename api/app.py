#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240


#import libraries
import os
import io
import json
from functools import wraps

from flask import Flask, request, jsonify, redirect, session
from firebase_admin import credentials, firestore, initialize_app, auth
import firebase_admin
from flask_cors import CORS
import pyrebase
from werkzeug.utils import secure_filename

#from face_encodings import search_similar_image, store_encodings, check_face_encodings
from data import check_encodings, search_similar_image

import cv2
import numpy

app = Flask(__name__)

firebase_admin.delete_app(firebase_admin.get_app())

cred = credentials.Certificate('fbAdminConfig.json')
default_app = firebase_admin.initialize_app(cred)

#auth = auth()

CORS(app)

db_connect = firestore.client()
todo_ref = db_connect.collection('todos')  #sample collections ##############

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))


#signup api

@app.route('/signup',methods = ['POST'])

def signup():

    email = request.json['email']    #get the email from json
    password = request.json['password'] #get the password from json
    
    #check condition
    if email is None or password is None:
       return jsonify({'message' : 'username and password must not in blank'}), 400
    
    #try - adding email and password to firebase, generate idToken, and send verification email
    try:

        #create user with given email and password
        user = auth.create_user(email = email, password = password)
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        
        firebase.auth().send_email_verification(user['idToken'])  #send verification email

        return jsonify({'idToken': user['idToken'], 'message': f'Successfully created user and send verification link please activate your account '}), 200
    

    #check if email and password already exists
    except:
    
        if email:
            emailexists = auth.get_user_by_email(email)
    
            if(emailexists.uid):
                return jsonify({'message': 'user already exists '}), 400
    
        else:
            return jsonify({'message': 'error creating in user'}), 401




#login api

@app.route('/login', methods = ['POST'])

def login():
    
    email = request.json['email'] 
    password = request.json['password']
    
    #check if email and password are entered
    if email is None or password is None:
        return jsonify({'message': 'username and password must not to be empty'}), 400
    
    
    try:

        #fetching user details from firebase
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        

        #fetch localId of the user to check whether the email id is verified or not
        check_user_local_id = user['localId']
        
        authorized_user = auth.get_user(check_user_local_id)
        
        #check if the user verified email or not      
        is_email_verified = authorized_user.email_verified

        if is_email_verified:
            return user
        
        else:
            return jsonify({'message': 'please verify your account with your mailId'}), 401
    
    
    #invalid credentials
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


if __name__ == '__main__':

    app.run(debug = True)

