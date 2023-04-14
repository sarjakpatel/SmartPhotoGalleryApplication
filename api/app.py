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

<<<<<<< Updated upstream
=======
db_connect = firestore.client()
todo_ref = db_connect.collection('todos')  #sample collections ##############

firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))
>>>>>>> Stashed changes

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
    app.run(debug=True)

