from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.manager import UserManager



class User(AbstractUser):

    username = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    is_verfied = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True 

    @property  
    def is_staff(self):
        "Is the user a admin member?"
        return self.is_admin

