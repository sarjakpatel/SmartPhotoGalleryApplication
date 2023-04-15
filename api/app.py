#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240

import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
<<<<<<< Updated upstream
from flask_cors import CORS
import io
import json
from firebase_admin import auth
=======
from werkzeug.utils import secure_filename
import os  
from flask import Flask, render_template, request
from ocr_core import ocr_core

#from face_encodings import search_similar_image, store_encodings, check_face_encodings
from data import check_encodings, search_similar_image

import cv2
import numpy

app = Flask(__name__)

firebase_admin.delete_app(firebase_admin.get_app())

cred = credentials.Certificate('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbAdminConfig.json')
default_app = firebase_admin.initialize_app(cred)
>>>>>>> Stashed changes


app=Flask(__name__)
cred = credentials.Certificate("/home/vishnu-yeruva/Documents/Edu/CMPE295B/Project/SmartPhotoGalleryApplication/api/fbAdminConfig.json")
default_app=firebase_admin.initialize_app(cred)
CORS(app)
db = firestore.client()
todo_ref=db.collection('todos')  #sample collections
pb = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE295B/Project/SmartPhotoGalleryApplication/api/fbconfig.json')))

db_connect = firestore.client()
todo_ref = db_connect.collection('todos')  #sample collections ##############

firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))

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
            return jsonify({'message':'please verify your account with your mailId'}),401
    except:
        return jsonify({'message':'invalid crendentails or user does not exist'}),403
<<<<<<< Updated upstream
=======

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
    
    
    elif img_matrix is None:
        return jsonify({'message': 'upload file'}), 400

    elif email and img_matrix:
        output_urls, keys, match1 = search_similar_image(email, img_matrix)
        

        return jsonify({'list of similar images': output_urls}), 200
    

###########################################################################

UPLOAD_FOLDER = '/static/uploads/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

def allowed_file(filename):  
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():  
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():  
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

##########################################################################


>>>>>>> Stashed changes
if __name__ == '__main__':

    app.run(debug = True)



