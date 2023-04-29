#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240


#import libraries
import os
import io
import json
from functools import wraps
from PIL import Image

from flask import Flask, request, jsonify, redirect, session, send_file
from firebase_admin import credentials, firestore, initialize_app, auth
import firebase_admin
from flask_cors import CORS
import pyrebase
from werkzeug.utils import secure_filename

from data import *

from PIL import Image
from io import BytesIO
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

    token = request.json['user-token']
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
        print(email)
        is_encoding_stored = check_encodings(email, image_url, token)

        if is_encoding_stored:
            print("encoding found")
            return jsonify({'message': 'stored encodings'}), 200
        
        else:
            print("no encoding found")
            return jsonify({'message': 'no encodings found in the image'}), 204


@app.route('/image-search', methods = ['POST'])

def search_similar_image1():
    
    token = request.form.get('user-token')
    email = request.form.get('email')
    #email = 'rajvi.shah@sjsu.edu'
    #file = request.files['file']
    # print(request)
    print(email)
    # print(type(request.files['file']))
    image = Image.open(request.files['file'])
    # print(type(image))
    # print(image)
    
    # img_matrix = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

    if email is None and image is None:
        return jsonify({'message': 'email must not to be empty and upload file'}), 400
    
    elif email is None:
        return jsonify({'message': 'email must not to be empty'}), 400
    
    elif image is None:
        return jsonify({'message': 'upload file'}), 400

    elif email and image:
        print(email)
        output_urls, keys, match1, flag = search_similar_image(email, image)
        

        return jsonify({'list of similar images': output_urls}), 200


@app.route('/face-analysis', methods = ['POST'])
@isAuthenticated
def face_analysis():
    image = Image.open(request.files['file'])
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    return jsonify({'Face Analysis': analyze_face(image)}), 200

   
@app.route('/emotion-detection', methods = ['POST'])
@isAuthenticated
def detect_emotion():
    image = Image.open(request.files['file'])
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    return jsonify({'emotion detected' : compute_emotion(image)}), 200
        

@app.route('/text-extraction', methods = ['POST'])

def get_text():

    if 'file' not in request.files:
        return jsonify({'message': 'Please upload file'}), 400
    img_file = request.files['file']
    if img_file is None:
        return jsonify({'message': 'Please upload file'}), 400
    img_text = ocr_core(filename=img_file)
    return jsonify({'ocr_text':img_text}), 200



@app.route('/deblur-image', methods = ['POST'])

def deblur_image():
    image = Image.open(request.files['file'])
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    else:
        output = deblur_image1(image)

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        output.save(buffer, format="JPEG")
        buffer.seek(0)

        # Return the image file in the response
        return send_file(buffer, mimetype="image/jpeg")



@app.route('/image-cartoonify', methods = ['POST'])

def image_cartoonify():
    image = Image.open(request.files['file'])
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    else:
        try: 
            output = image_cartoonify1(image)

            # Save the image to a BytesIO buffer
            buffer = BytesIO()
            output.save(buffer, format="JPEG")
            buffer.seek(0)

            # Return the image file in the response
            return send_file(buffer, mimetype="image/jpeg")
        
        except:
            return jsonify({'Output': "Model Error"}), 400

'''
@app.route('/image-question', methods = ['POST'])

def image_question():
    question = request.form.get('text')
    #question = 'How many cats are there?'
    image = Image.open(request.files['file'])
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    else:
        output = image_question1(image, question)

        return jsonify({'Output': output}), 200
        #return send_file(img)
'''

@app.route('/remove-bg', methods = ['POST'])
#output in 35 seconds
def remove_bg():
   
    image = Image.open(request.files['file'])

    if image is None:
        return jsonify({'message': 'upload file'}), 400
    
    else:
        output = remove_img_bg(image)

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        output.save(buffer, format="JPEG")
        buffer.seek(0)

        # Return the image file in the response
        return send_file(buffer, mimetype="image/jpeg")


@app.route('/image-sketch', methods = ['POST'])
#output in 5 seconds
def image_sketch():
   
    image = Image.open(request.files['file'])

    if image is None:
        return jsonify({'message': 'upload file'}), 400
    
    else:
        output = img_sketch(image)

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        output.save(buffer, format="JPEG")
        buffer.seek(0)

        # Return the image file in the response
        return send_file(buffer, mimetype="image/jpeg")


@app.route('/generate-image', methods=['POST'])

def generate_image():

    text = request.form.get('text')
    
    try:

        output = generate_image1(text)

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        output.save(buffer, format="JPEG")
        buffer.seek(0)

        # Return the image file in the response
        return send_file(buffer, mimetype="image/jpeg")
    
    except:
        return jsonify({'Output': "Access Error"}), 400


    #return jsonify({'image': output})


@app.route('/image-filter', methods = ['POST'])
@isAuthenticated
def apply_filter():
    image = Image.open(request.files['file'])
    brightness_control = int(request.form.get('brightness_control'))
    contrast_control = int(request.form.get('contrast_control'))
    saturation_control = int(request.form.get('saturation_control'))
    hue_control = int(request.form.get('hue_control'))
    vignette_control = int(request.form.get('vignette_control'))
    sharpen_control = int(request.form.get('sharpen_control'))
    effect_control = request.form.get('effect_control')
    if image is None:
        return jsonify({'message': 'upload file'}), 400
    else:
        try:

            img = photoEditor(image, brightness_control, contrast_control, saturation_control, hue_control, vignette_control, sharpen_control, effect_control)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            
            # Return the image file in the response
            return send_file(buffer, mimetype="image/jpeg")
            #return jsonify({'Output': img}), 200
        except:
            return jsonify({'Brightness' : brightness_control, 'Contrast' : contrast_control,
                            'Saturation' : saturation_control, 'Hue' : hue_control,
                            'Vignette' : vignette_control, 'Sharpen' : sharpen_control,
                            'Effect' : effect_control}), 400


if __name__ == '__main__':
    app.run(debug=True)