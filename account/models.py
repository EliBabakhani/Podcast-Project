from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    password=models.CharField(max_length=100)
    username=models.CharField(max_length=50)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]