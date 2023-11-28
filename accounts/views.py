from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from .models import User
from .serializer import *
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='1/s', block=True), name='dispatch')
class UserList(generics.ListAPIView):
    # @method_decorator(ratelimit(key=ip, rate='1/s' block=True))
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Register Firebase

class FirebaseRegisterViewset(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet
                          ):
    queryset = User.objects.all()
    serializer_class = FirebaseRegisterSerializer
    authentication_classes = ()
    
    def get_queryset(self):
        return self.queryset.filter(pk=self.kwargs['pk'])

# End Register Firebase    

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    
class UserLoginView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer


@method_decorator(ratelimit(key='ip', rate='2/m', block=True), name='dispatch')
class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = UserOTPSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            user.send_otp()
            return Response({"message" : "OTP successfully sent"}, 200)
        except User.DoesNotExist:
            return Response({"message" : "User not found"}, 404)

class VerifyOTPView(generics.CreateAPIView):
    serializer_class = UserOTPSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = User.objects.get(email=email)
            if user.verify_otp(otp):
                return Response({"message" : "OTP successfully verified"}, 200)
            else:
                return Response({"message" : "Expired OTP or OTP is wrong"}, 400)
        except User.DoesNotExist:
            return Response({"message" : "User not found"}, 404)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserOTPSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Password dan konfirmasi password tidak sesuai"})
        
        try:
            user = User.objects.get(email=email)
            otp = user.otp
            if user.verify_otp(otp):
                user.change_password(password)
                return Response({"message" : "Password berhasil diubah"}, 200)
            else:
                return Response({"message" : "Expired OTP or OTP is wrong"}, 400)
        except User.DoesNotExist:
            return Response({"message" : "User not found"}, 404)

# @method_decorator(ratelimit(key='ip', rate='15/m', block=True), name='dispatch')
class UserProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        img = user.img
        username = user.username
        email = user.email
        return Response(
            {
                "img"       : img,
                "username" : username,
                "email"         : email,
            }, 200
        )
            
    def update(self, request, *args, **kwargs):
        user = request.user

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "detail": "Profile berhasil diubah",
                }, 200
            )        
        print(serializer.validated_data)
        return Response({"message" : "Unauthorized"}, 401)