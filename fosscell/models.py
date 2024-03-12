from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self,institution,email,password,is_staff,is_superuser,is_registered,**extra_fields):
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
            is_registered=is_registered,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,institution,email,password,**extra_fields):
        return self._create_user(institution,email,password,False,False,False,**extra_fields)
    
    def create_superuser(self,institution,email,password,**extra_fields):
        user=self._create_user(institution,email,password,True,True,True,**extra_fields)
        return user
    

class Institution(models.Model):
    name = models.CharField(max_length=250,unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=254,unique=True)
    institution = models.CharField(max_length=250)
    name=models.CharField(max_length=254,null=True,blank=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    last_login=models.DateTimeField(null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=['institution']

    objects=UserManager()

    def get_absolute_url(self):
        return "/core/%i/" % (self.pk)

    
class ProgramType(models.Model):
    values = models.CharField(max_length=75)

    def __str__(self):
        return self.values
    


class ProgramMode(models.Model):
    values = models.CharField(max_length=75)

    def __str__(self):
        return self.values
    

class AudienceType(models.Model):
    values = models.CharField(max_length=100)

    def __str__(self):
        return self.values

def validate_file_size(value):
    limit = 500 * 1024
    if value.size>limit:
        raise ValidationError(f"File size cannot exceed 500 KB")
    

class Activity(models.Model):
    institution_name = models.ForeignKey(Institution,on_delete=models.CASCADE)
    program_name = models.CharField(max_length=200)
    program_type = models.ForeignKey(ProgramType,on_delete = models.PROTECT)
    program_mode = models.ForeignKey(ProgramMode,on_delete = models.PROTECT)
    auience_type = models.ForeignKey(AudienceType,on_delete = models.PROTECT)
    participant_count = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    date_time = models.DateTimeField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    proposed_venue = models.CharField(max_length=255,null=True,blank=True)
    need_assistance = models.BooleanField()
    kind_of_assistance = models.TextField(null=True,blank=True)
    notified_others = models.BooleanField()
    website_link = models.CharField(max_length=255,null=True,blank=True)
    supporting_documents = models.FileField(upload_to='supporting_documents/',
                                            validators=[
                                                FileExtensionValidator(allowed_extensions=['pdf']),
                                                validate_file_size,
                                            ]
                                            )
    status = models.BooleanField(null=True)
    remarks = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.program_name



