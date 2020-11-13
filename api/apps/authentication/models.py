import datetime
import uuid
from django.core.validators import FileExtensionValidator
from django.template.loader import render_to_string
from django.db import models
from django.utils import timezone
from django.core.signing import (TimestampSigner, 
        b64_encode, 
        b64_decode, 
        BadSignature,
        force_bytes)
from django.core.mail import EmailMessage
from django.contrib.auth.models import UserManager, AbstractUser
from django.conf import settings
USER_TYPES = {
    "ADMIN": 1,
    "MODERATOR": 2,
    "USER": 3,
}

class SocialUser(models.Model):
    id = models.CharField(primary_key=True,max_length=256,unique=True,editable=True)
    email = models.EmailField(max_length=64, blank=False, unique=True)
    first_name = models.CharField(max_length=64, blank=False, default="")
    last_name = models.CharField(max_length=64, blank=False, default="") 
    photo_url = models.CharField(max_length=512,blank=False,default="")
    provider = models.CharField(max_length=24,blank=False,default="")

    def __str__(self):
        return self.email

    def __unicode__(self):
        return self.email

class StdUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, user_type=3, **extra_fields):
        if user_type == USER_TYPES["USER"]:
            extra_fields.setdefault('is_moderator', False)
            extra_fields.setdefault('is_admin', False)
            extra_fields.setdefault('is_active', False)

        elif user_type == USER_TYPES["ADMIN"]:
            extra_fields.setdefault('is_admin', True)
            extra_fields.setdefault('is_active', True)
        
        elif user_type == USER_TYPES["MODERATOR"]:
            extra_fields.setdefault('is_moderator', True)
            extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, **extra_fields)


# Base user class
class StdUser(AbstractUser):
    objects = StdUserManager()

    id = models.UUIDField(primary_key=True,unique=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=64, blank=True, unique=False)
    # We need this, because in AbstractUser 'unique=True'
    email = models.EmailField(max_length=64, blank=False, unique=True)  # ivanov@gmail.com

    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=64, blank=False, default="")  # Ivan
    last_name = models.CharField(max_length=64, blank=False, default="")  # Ivanov
    patronymic = models.CharField(max_length=64, blank=True, default="")  # Ivanovych
    avatar = models.ImageField(upload_to='authentication/', blank=True,null=True, max_length=1000,
                               default='authentication/default.png', validators=[FileExtensionValidator(["jpeg", "png", "svg", "jpg", "bmp"])])  # select image
    bio = models.CharField(max_length=512, blank=True, default="")
    date_of_birth = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=64, blank=True, default="man") # Man/Wpman
    
    news_subscription = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)  # can login
    is_admin = models.BooleanField(default=False)  # admin
    is_moderator = models.BooleanField(default=False) # moderator

    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    
    social_user = models.ForeignKey(SocialUser,
            on_delete=models.CASCADE,default=None,
        to_field="email",null=True,blank=True)
    
    code = models.CharField(max_length=256, blank=True, default="")
    USERNAME_FIELD = 'email'  # Email as username
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.get_full_name()

    class Meta:
        permissions = [('read_news', 'Читати новини',),]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_full_name(self):
        """ Returns full name with spaces between """
        full_name = "%s %s %s" % (self.first_name, self.patronymic, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """ Returns short name """
        short_name = "%s" % self.first_name
        return short_name.strip()

    def get_verification_code(self, email):
        # verification token 
        signer = TimestampSigner()
        return b64_encode(bytes(signer.sign(email), encoding='utf-8'))
        
    @classmethod
    def verify_email(self, code):
        if code:
            signer = TimestampSigner()
            try:
                code = code.encode('utf-8')
                max_age = datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED).total_seconds()
                code = force_bytes(code)
                code = b64_decode(code)
                code = code.decode()
                email = signer.unsign(code, max_age=max_age)
                user = StdUser.objects.get(**{StdUser.USERNAME_FIELD: email, 'is_active': False})
                user.is_active = True
                user.code = "None code"
                user.save()
                
                return True, ('Your account has been activated.')  
            except (BadSignature, StdUser.DoesNotExist, TypeError, UnicodeDecodeError):
                raise ValueError('Error')
            return False, ('Activation link is incorrect, please resend request')
        else:
            raise ValueError('No code')

    @classmethod
    def verify_password(self, code, password):
        if code:
            signer = TimestampSigner()
            try:
                code = code.encode('utf-8')
                max_age = datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED).total_seconds()
                code = force_bytes(code)
                code = b64_decode(code)
                code = code.decode()
                email = signer.unsign(code, max_age=max_age)
                 
                user = StdUser.objects.get(**{StdUser.USERNAME_FIELD: email})
                user.set_password(password)
                user.code = 'None code'
                user.save()
                return True
            except (BadSignature, AttributeError, StdUser.DoesNotExist, TypeError, UnicodeDecodeError):
                raise ValueError('Error')
            return False, ('Activation link is incorrect, please resend request')
        else:
            raise ValueError('No code')

    def send_mail(self, email):
        verification_code = self.get_verification_code(email=email)
        context = {'user': self,
                   'VERIFICATION_URL': settings.VERIFICATION_URL,
                   'HOST': settings.ALLOWED_HOSTS[0],
                   'code': verification_code.decode(),
                   'link': datetime.datetime.today() + datetime.timedelta(days=settings.VERIFICATION_CODE_EXPIRED)   
                }
        
        msg = EmailMessage(subject='Підтвердіть свою особу на сайті',
                body=render_to_string('authentication/mail/verification_body.html', context),
                to=[email])
        msg.content_subtype = 'html'
        msg.send()

    def send_recovery_password(self, email):
        verification_code = self.get_verification_code(email=email)
        
        context = {'user': self,
                   'RECOVER_URL': settings.RECOVER_URL,
                   'HOST': settings.ALLOWED_HOSTS[0],
                   'code': verification_code.decode(),
                   'link': datetime.datetime.today() + datetime.timedelta(days=settings.RECOVER_CODE_EXPIRED)
                    }
        msg = EmailMessage(subject='subject',
                body=render_to_string('authentication/mail/reset_body.html', context),
                to=[email])
        msg.content_subtype = 'html'
        msg.send()

    # Saving
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
