from django.shortcuts import render
from .models import Account, UserType
from rest_framework import generics
from .serializers import SignUpSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from freelancers.models import FreelancerProfile
from users.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from .token import create_jwt_pair_tokens
from .otp import send_otp
import datetime

# Create your views here.


#SignUp 
class SignUpView(generics.GenericAPIView):
    serializer_class    = SignUpSerializer
    permission_classes  = [AllowAny]

    def post(self, request: Request):
        data = request.data

        serializer  = self.serializer_class(data=data)
        user_type   = request.data.get('user_type')
        email       = request.data.get('email')

        if serializer.is_valid():
            serializer.save()

            if user_type == 'Freelancer':
                user = Account.objects.get(email = email)
                user_type = UserType.objects.get(user_type_name = 'Freelancer')
                user.user_type = user_type
                user.save()
                FreelancerProfile.objects.create(freelancer = user)
                phone_number = data.get('phone_number')
                email = data.get('email')
                username = data.get('username')
                send_otp(username, email)

            elif user_type == 'User':
                user = Account.objects.get(email = email)
                user_type = UserType.objects.get(user_type_name = 'User')
                user.user_type = user_type
                user.save()
                UserProfile.objects.create(user = user)
                phone_number = data.get('phone_number')
                email = data.get('email')
                username = data.get('username')
                send_otp(username, email)

            else:
                print('neither freelancer nor user')

            response = {
                'message' : 'User Created Successfully',
                'otp' : True
            }
            return Response(data = response, status = status.HTTP_201_CREATED)
        
        else:
            print(serializer.errors)
            errorMessage = "Error occurred Please check your inputs"
            if Account.objects.filter(email=email).exists():
                errorMessage = "Email is already taken"
            if Account.objects.filter(phone_number=request.data.get('phone_number')).exists():
                errorMessage = "Phone number already Taken"
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)
        

#OptVerification
class Verify_otpView(APIView):
    def post(self, request: Request):
        data = request.data
        check_otp = data.get('otp')
        email = data.get('email')

        try:
            user = Account.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"Failed": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        stored_otp = user.otp

        if stored_otp == check_otp:
            user.is_verified = True
            user.otp = ""
            user.save()

            return Response(
                data={'Success': 'User is verified', 'is_verified': True},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Failed": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )
        

#Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_verified == True:
                tokens = create_jwt_pair_tokens(user)
                refresh_token = RefreshToken(tokens['refresh'])

                response = {
                    "message": "Login Successful",
                    "access_token": tokens['access'],
                    "refresh_token": tokens['refresh'],
                    "token_expiry": refresh_token['exp'],
                    "is_login": True,
                    "user": {
                        "user_id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "username": user.username,
                        "phone_number": user.phone_number,
                        "email": user.email,
                        "user_type": user.user_type.user_type_name,
                        "is_active": user.is_active,
                        "is_profile": user.is_profile
                    }
                }
                return Response(data=response, status=status.HTTP_200_OK)

            
            else:
                response = {
                    "message" : "user is not verified"
                }
                return Response(data=response, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        else:
            return Response(data={"message" : "Invalid email or password !"}, status=status.HTTP_400_BAD_REQUEST)