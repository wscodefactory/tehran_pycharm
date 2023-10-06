from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, id, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Regular user must have is_staff=True.')

        return self.model.objects.create(id=id, **extra_fields)

    def create_superuser(self, id, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # 비밀번호를 해싱하여 저장
        extra_fields['password'] = make_password(password)

        return self.create_user(id=id, **extra_fields)

class User(AbstractUser):
    objects = CustomUserManager()

    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=128) # 해싱을 위한 크기 확보 필요 일반적으로 128을 쓴다고 함
    email = models.EmailField(max_length=45)
    name = models.CharField(max_length=45)

    username = None

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['password', 'email', 'name']
