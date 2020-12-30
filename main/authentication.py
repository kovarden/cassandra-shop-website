from django.contrib.auth.models import AbstractBaseUser
import hashlib
from django.contrib.auth import authenticate
from django.conf import settings
from .models import *


class MyBackend(object):
    def authenticate(self, request, email=None, password=None):
        salt = 'hiu4iof3bih'
        hashed_password = hashlib.md5(f"{password.encode('utf-8')}{salt}".encode('utf-8')).hexdigest()
        try:
            user = UserByEmail.objects.get(email=email, password=hashed_password)
            user.is_active = True
            return user
        except UserByEmail.DoesNotExist:
            return None

    # def authenticate(self, request, id=None, token=None):
    #     salt = 'hiu4iof3bih'
    #     hashed_password = hashlib.md5(f"{password.encode('utf-8')}{salt}".encode('utf-8')).hexdigest()
    #     try:
    #         user = UserByEmail.objects.get(email=email, password=hashed_password)
    #         user.is_active = True
    #         return user
    #     except UserByEmail.DoesNotExist:
    #         return None

    def get_user(self, user_id):
        print('get_user')
        try:
            return UserById.objects.get(id=user_id)
        except UserById.DoesNotExist:
            return None