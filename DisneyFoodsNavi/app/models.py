from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    groups = None
    user_permissions = None
    username = None
    
    nickname = models.CharField(max_length=64)
    email = models.EmailField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    USERNAME_FIELD = "nickname"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]
    
    
    class Meta:
        db_table = "users"