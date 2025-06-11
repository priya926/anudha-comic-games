import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Check if Firebase is already initialized

if not firebase_admin._apps:
    # cred = credentials.Certificate("anudhadb-firebase-adminsdk-fbsvc-b636f66480.json")   #for running on local server uncomment it and comment next line
    cred = credentials.Certificate("/etc/secrets/anudhadb-firebase-adminsdk-fbsvc-b636f66480.json")   
    firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()