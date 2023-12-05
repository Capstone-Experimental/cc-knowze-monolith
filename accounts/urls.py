from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from .views import *

app_name = 'accounts'
router = routers.DefaultRouter()

router.register(r'firebase-register', FirebaseRegisterViewset, basename='firebase_register')

urlpatterns = [
    # virwset
    path(r'', include(router.urls)),
    
    # all users
    # path('users/', UserList.as_view(), name='users'),

    # login and registration
    # path('login/', UserLoginView.as_view(), name='login'),
    # path('register/', UserRegistrationView.as_view(), name='register'),
        
    # refresh token
    # path('refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    # forgot password
    # path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    # path('otp-verification/', VerifyOTPView.as_view(), name='otp_verification'),
    # path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # edit profile and change password
    path('profile/', UserProfileView.as_view(), name='profile'),
]