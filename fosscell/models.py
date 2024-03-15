from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator
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
    

class Category(models.Model):
    name=models.CharField( max_length=250)

    def __str__(self):
        return self.name
    


class UniversityBoard(models.Model):
    name=models.CharField( max_length=250)

    def __str__(self):
        return self.name
    


def validate_file_size(value):
    limit = 500 * 1024  # 500 KB in bytes
    if value.size > limit:
        raise ValidationError(f"File size cannot exceed 500 KB")


# inst_details=User.objects.last()
class InstitutionReg(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    institution_details=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    university=models.ForeignKey(UniversityBoard,on_delete=models.CASCADE)
    official_mail=models.EmailField(max_length=200)
    land_no=models.CharField(max_length=15)
    pincode=models.IntegerField()
    district=models.CharField(max_length=150)
    state=models.CharField(max_length=150)
    zone=models.CharField(max_length=150)
    address=models.TextField()
    head_insti=models.CharField(max_length=150)
    designation=models.CharField(max_length=150)
    Email=models.EmailField(max_length=200)
    mobile_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Mobile number must be 10 digits long and start with a digit between 6 and 9.',
                code='invalid_mobile_number'
            ),
        ],
        help_text='Enter your mobile number without the country code.'
    )
    member_icfoss=models.BooleanField(default=False)
    member_since=models.DateTimeField(null=True,blank=True)
    approval_certificate = models.FileField(
        upload_to='approval_certificate/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf']),
            validate_file_size
            # MaxFileSizeValidator(limit_bytes=500 * 1024)  # 50 KB limit
        ]
    )
    status=models.BooleanField(null=True, blank=True)
    remarks = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.institution_details
    



class FossAdvisor(models.Model):
    uid=models.ForeignKey(User,models.CASCADE)
    advisor_name=models.CharField(max_length=150)
    advisor_designation=models.CharField(max_length=150)
    advisor_Email=models.EmailField(max_length=200)
    advisor_mobile_number = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Mobile number must be 10 digits long and start with a digit between 6 and 9.',
                code='invalid_mobile_number'
            ),
        ],
        help_text='Enter your mobile number without the country code.'
    )
    advisor_member_icfoss=models.BooleanField(default=False)
    advisor_member_since=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return self.advisor_name
    
class Members(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    uniqueid=models.CharField(max_length=255)
    member_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=10,
                         validators=[
                RegexValidator(
                    regex=r'^[6-9]\d{9}$',
                    message='Mobile number must be 10 digits long and start with a digit between 6 and 9.',
                    code='invalid_mobile_number'
            ),
        ],
        help_text='Enter your mobile number without the country code.'    
                             )
    department = models.CharField(max_length=255)
    semester = models.IntegerField()
    joining_date = models.DateField()
    course_end_date = models.DateField()
    def __str__(self):
        return self.name
    
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
    uid = models.ForeignKey(User,on_delete=models.CASCADE)
    institution_name = models.ForeignKey(Institution,on_delete=models.CASCADE)
    program_name = models.CharField(max_length=200)
    program_type = models.ForeignKey(ProgramType,on_delete = models.PROTECT)
    program_mode = models.ForeignKey(ProgramMode,on_delete = models.PROTECT)
    audience_type = models.ForeignKey(AudienceType,on_delete = models.PROTECT)
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



