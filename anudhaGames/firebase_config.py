import firebase_admin
from firebase_admin import credentials, Firestore

# Check if Firebase is already initialized

if not firebase_admin._apps:
    cred = credentials.Certificate("/etc/secrets/anudhadb-firebase-adminsdk-fbsvc-b636f66480.json")   
    firebase_admin.initialize_app(cred)

# Firestore database instance
db = Firestore.client()