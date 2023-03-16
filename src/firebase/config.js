import firebase from 'firebase/compat/app';
import 'firebase/compat/storage';
import 'firebase/compat/firestore';

var firebaseConfig = {
    "apiKey": "AIzaSyDG5VMPk7sjOuFbLecg_H752oiZr0KIXwk",
    "authDomain": "user-auth-42504.firebaseapp.com",
    "projectId": "user-auth-42504",
    "storageBucket": "user-auth-42504.appspot.com",
    "messagingSenderId": "1095641663469",
    "appId": "1:1095641663469:web:f9d740e2307c28fef2c9e4",
    "measurementId": "G-W1JKWCE33S",
    "databaseURL": "https://user-auth-42504-default-rtdb.firebaseio.com"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

const projectStorage = firebase.storage();
const projectFirestore = firebase.firestore();
const timestamp = firebase.firestore.FieldValue.serverTimestamp;

export { projectStorage, projectFirestore, timestamp };