from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):


    def create_user(self, email,username, password,password2=None):

        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email),username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_superuser(self, email,username,password,password2):

        """creates and save a new super User"""
        user = self.create_user(email=email,username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user