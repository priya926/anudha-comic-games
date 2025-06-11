import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Check if Firebase is already initialized
if not firebase_admin._apps:
    firebase_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    if firebase_json:
        cred_dict = json.loads(firebase_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise ValueError("Firebase credentials not found in environment.")

# Firestore database instance
db = firestore.client()