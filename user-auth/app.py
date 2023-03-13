# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:34:11 2023

@author: HP
"""

#reference: https://medium.com/makedeveasy/authenitcation-using-python-flask-and-firestore-1958d29e2240


#import libraries
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import firebase_admin
import pyrebase
from flask_cors import CORS
import io
import json
from firebase_admin import auth


app = Flask(__name__)

cred = credentials.Certificate("fbAdminConfig.json")
default_app = firebase_admin.initialize_app(cred)

CORS(app)

db = firestore.client()
todo_ref = db.collection('todos')  #sample collections

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))




@app.route("/")  #basic api

def home():
    return "Go to Sign Up or Sign In page"




#signup api
@app.route('/signup', methods = ['POST'])
  
def signup():
    
    email = request.json['email']    #get the email from user
    password = request.json['password'] #get the password from user
    
    #check condition
    if email is None or password is None:
        return jsonify({'message' : 'username and password must not in blank'}), 400
    
    
    #try - adding email and password to firebase, generate idToken, and send verification email
    try:
        
        user = auth.create_user(email = email, password = password) #create user with given email and password
        user = firebase.auth().sign_in_with_email_and_password(email, password) 
        
        firebase.auth().send_email_verification(user['idToken']) #send verification email
        
        return jsonify({'idToken': user['idToken'], 'message': f'Successfully created user and send verification link please activate your account '}),200
    
    #check if email and password already exists
    except:
        
        if email:
            
            email_exists = auth.get_user_by_email(email)
            
            if(email_exists.uid):
                return jsonify({'message': 'user already exists '}), 400
        
        else:
            return jsonify({'message': 'error creating in user'}), 400





#signin api
@app.route('/signin', methods = ['POST'])

  
def signin():
    
    email = request.json['email'] 
    password = request.json['password']
    
    #check if email and password are entered
    if email is None or password is None:
        
        return jsonify({'message':'username and password must not to be empty'}), 400
    
    
    try:
        
        #fetching user details from firebase
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        
        #print(user)
        
        '''
        arr=''
        
        for x in user:
            if x == 'localId':
                arr=(user[x])
        '''
        #fetch localId of the user to check whether the email id is verified or not
        check_user_local_id = user['localId']
        
        authorized_user = auth.get_user(check_user_local_id)
        
        #check if the user verified email or not      
        is_email_verified = authorized_user.email_verified
     
        
        if is_email_verified:
            return user
        
        else:
            return jsonify({'message': 'please verify your account with your mailId'}), 400
    
    
    #invalid credentials
    except:
        return jsonify({'message': 'invalid credentials or user does not exist'}), 400




#main function
if __name__ == '__main__':
    app.run(debug=True)

