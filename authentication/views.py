from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from authentication.utils import *
from authentication.serializer import *
from authentication.models import *



# generating Token manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class Creatsuperuserview(APIView):
    def post (self,request):
        serializer = superuserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'msg':'Your Registration Successful'},
                status = status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserRegistrationView(APIView):
    def post (self,request):

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            email = serializer.data['email']
            WelcomeEmailMessage(email=email).start()
            return Response(
                {'msg': 'Registration Successfull'},
                status = status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            send_otp_via_email(serializer.data['email'])
            if user is not None:
                return Response(
                    {'msg': 'OTP send to your email'},
                    status = status.HTTP_200_OK
                )

            else:
                return Response(
                    {'errors': {'non_field_error': ['Email or Password is not valid']}},
                    status = status.HTTP_400_BAD_REQUEST)



class VerifyOTP(APIView):
    def post(self,request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)

            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']

                user = User.objects.filter(email=email)

                if not user.exists():
                        return Response(
                        {
                            'status' : 400,
                            'message' : 'Somethimg went wrong',
                            'data': 'invalid email',

                        }
                    )

                if not user[0].otp == otp:
                        return Response(
                        {
                            'status' : 400,
                            'message' : 'Somethimg went wrong',
                            'data': 'wrong otp',

                        }
                    )

                user = user.first()
                user.is_verfied = True
                user.save()
                token = get_tokens_for_user(user)
                return Response(
                            {
                                'token':token,
                                'status' : 200,
                                'message' : 'Acount Verified',
                            }
                    )


            return Response(
                    {
                        'status' : 400,
                        'message' : 'Somethimg went wrong',
                        'data': serializer.errors,

                    }
                )

        except Exception as w:
            return Response(str(w))       




class PasswordChangeView(APIView):
    def post(self,request,format=None):
        serializer = PasswordChangeSerializer(data=request.data,
                                             context={'user': request.user})

        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Change Successfull'},
            status = status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)