import firebase_admin
from pathlib import Path
import os
from firebase_admin import credentials
from firebase_admin import auth
from rest_framework import authentication
from rest_framework import exceptions
BASE_DIR = Path(__file__).resolve().parent.parent

FIREBASE_DIR = os.path.join(BASE_DIR, 'util/cred.json')

credential = credentials.Certificate(FIREBASE_DIR) 

firebase_admin.initialize_app(credential)
# firebase_admin.initialize_app()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if not authorization_header:
            return None

        # Header is in the format "Bearer token"
        token = authorization_header.split(' ')[1]
        # print(token)

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            print(uid)
            return (decoded_token, None)  # Authentication successful
        except:
            raise exceptions.AuthenticationFailed('Invalid token')