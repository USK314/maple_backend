import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore


cred = credentials.Certificate("cert.json")

firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'garigari-stagram.appspot.com',
    'projectId': 'garigari-stagram',
})


bucket = storage.bucket()

db = firestore.client()
