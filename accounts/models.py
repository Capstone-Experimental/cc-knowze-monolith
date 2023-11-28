import uuid
import math
import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractUser

from django.conf import settings
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, username, email = None, password = None):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        
        user = self.model(
            username = username,
            email = self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username = username,
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def generateOTP() :
        digits = "0123456789"
        OTP = ""
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
        return OTP
class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    img = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
    def has_module_perms(self, app_label):
        return True
    
    def send_otp(self):
        otp = generateOTP()
        self.otp = otp
        self.otp_expiration = timezone.now() + timezone.timedelta(minutes=5)
        self.save()
        
        send_mail(
            'Kode OTP',
            f'Berikut adalah kode OTP Anda: {otp}',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )
    
    def verify_otp(self, otp):
        current_time = timezone.now()
        if self.otp == otp and current_time <= self.otp_expiration:
            return True
        return False

    def change_password(self, password):
        self.set_password(password)
        self.save()