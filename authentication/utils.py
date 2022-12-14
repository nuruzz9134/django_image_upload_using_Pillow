from authentication.models import User
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import threading
import random


class WelcomeEmailMessage(threading.Thread):

    def __init__(self , email):
        self.email=email
        threading.Thread.__init__(self)


    def run(self):

        subject = "registration success"
        message = "Welcome, You have registered. Please Login."
        email_from = settings.EMAIL_HOST
        email_message = EmailMessage(subject,message,email_from,[self.email])
        email_message.attach_file("/home/pranto/Desktop/Djangoprojects/email_otp_auth/new_file/welcome.jpg")
        email_message.send()






def send_otp_via_email(email):
        subject = 'Your account verification email'
        otp = random.randint(1000 , 9999)
        message = f'Your OTP number is :   {otp}'
        email_from = settings.EMAIL_HOST
        send_mail(subject , message , email_from , [email])
        user_obj = User.objects.get(email=email)
        user_obj.otp =otp
        user_obj.save()
