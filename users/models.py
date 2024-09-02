from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone_number=phone_number,

        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number,  password=None):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(default="", max_length=254)
    botStatus = models.BooleanField(default=False)
    total_listings = models.IntegerField(default=0)
    failed_listings_myhome = models.JSONField(default=list)
    failed_listings_ss = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    current_jwt_token = models.CharField(max_length=500, blank=True, null=True)  # Add this field

    objects = MyUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return self.phone_number





