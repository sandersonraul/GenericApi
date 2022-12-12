from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  username =  models.CharField(max_length=255)
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255, null=True) 
  is_staff = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']


