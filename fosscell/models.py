from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self,institution,email,password,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError("User must have an Email address")
        now=timezone.now()
        email = self.normalize_email(email)
        user=self.model(
            institution =institution,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,institution,email,password,**extra_fields):
        return self._create_user(institution,email,password,False,False,**extra_fields)
    
    def create_superuser(self,institution,email,password,**extra_fields):
        user=self._create_user(institution,email,password,True,True,**extra_fields)
        return user
    

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=254,unique=True)
    institution = models.CharField(max_length=250)
    name=models.CharField(max_length=254,null=True,blank=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    last_login=models.DateTimeField(null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=['institution']

    objects=UserManager()

    def get_absolute_url(self):
        return "/core/%i/" % (self.pk)

    