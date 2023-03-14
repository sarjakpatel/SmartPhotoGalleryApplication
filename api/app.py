#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240

import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
from flask_cors import CORS
import io
import json
from firebase_admin import auth


app=Flask(__name__)
cred = credentials.Certificate("fbAdminConfig.json")
default_app=firebase_admin.initialize_app(cred)
CORS(app)
db = firestore.client()
todo_ref=db.collection('todos')  #sample collections
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))


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
if __name__ == '__main__':
    app.run(debug=True)

