#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240

# import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
from flask_cors import CORS
import io
import json
from firebase_admin import auth


app=Flask(__name__)
cred = credentials.Certificate("/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbAdminConfig.json")
# default_app=firebase_admin.initialize_app(cred)
CORS(app)
db = firestore.client()
todo_ref=db.collection('todos')  #sample collections
pb = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))

db_connect = firestore.client()
todo_ref = db_connect.collection('todos')  #sample collections ##############

<<<<<<< Updated upstream
firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE 295-B/Project/api/fbconfig.json')))
=======
firebase = pyrebase.initialize_app(json.load(open('/home/vishnu-yeruva/Documents/Edu/CMPE295B/Project/SmartPhotoGalleryApplication/api/fbconfig.json')))


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
if __name__ == '__main__':

    app.run(debug = True)



