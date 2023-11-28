from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from django.core.files.storage import default_storage
from django.core.files import File
from google.cloud import storage
from django.core.files.base import ContentFile
from util.credentials import credentials
# refresh token
# from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'img']

## Firebase Register

from firebase.utils import check_token
from firebase_admin import auth

class FirebaseRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    img = serializers.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'img']
        
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email sudah terdaftar")
        
        firebase_uid = check_token(self.context.get('request', None))
        firebase_user = auth.get_user(firebase_uid)
        print("user : ", firebase_user)
        
        try:
            data['id'], created = User.objects.get_or_create(
                id=firebase_user.uid,
                # email=firebase_user.email,
            )
        except:
            raise serializers.ValidationError(
                {"detail": "id user dan phone number tidak cocok"})
        
        return data
    
## End Firebase Register

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, max_length=100, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, data):
        user = User.objects.create_user(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(write_only=True) 
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access', 'refresh']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None:
            raise serializers.ValidationError({"errors" : "Email or password is incorrect"})

        if len(data['password']) > 100:
            raise serializers.ValidationError({"errors" : "Password is too long"})
        
        if len(data['password']) < 8:
            raise serializers.ValidationError({"errors" : "Password is too short"})
        
        if not user.check_password(data['password']):
            raise serializers.ValidationError({"errors" : "Email or password is incorrect"})
        
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
        }
        # data['access_token'] = str(refresh.access_token)
        # data['refresh_token'] = str(refresh)

        # if operator login response must different
        # return data
        return response_data


class UserOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password', 'otp')

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)
    
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)
    img = serializers.ImageField(required=False)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        
        if validated_data.get('img') is not None:
            img_extension = validated_data.get('img').name.split('.')[-1]
            if img_extension.lower() not in ['png', 'jpg', 'jpeg']:
                raise serializers.ValidationError("Hanya file PNG, JPG, dan JPEG yang diizinkan.")
            
            gcs = storage.Client(credentials=credentials)
            bucket = gcs.get_bucket('go-mono')
            blob = bucket.blob(f'users/{instance.id}.{img_extension}') 
            blob.upload_from_string(
                validated_data.get('img').read(),
                content_type=validated_data.get('img').content_type
            )
            
            instance.img = f'https://storage.googleapis.com/go-mono/users/{instance.id}.{img_extension}'
            instance.save()
            
            old_img_path = instance.img
            if old_img_path and validated_data.get('img') and old_img_path != instance.img:
                # Hapus gambar lama dari Google Cloud Storage
                old_blob = bucket.blob(old_img_path.split('/')[-1])
                old_blob.delete()
                
        # if validated_data.get('img') is not None:
            
        #     old_img_path = instance.img.path
        #     if old_img_path and validated_data.get('img') and old_img_path != validated_data.get('img'):
        #         default_storage.delete(old_img_path)
        #         instance.img.save(validated_data.get('img').name, File(validated_data.get('img')))
        
        instance.save()
        return instance
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'img']