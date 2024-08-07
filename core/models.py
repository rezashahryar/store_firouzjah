from datetime import timedelta
from uuid import uuid4

import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import django.utils
import django.utils.timezone

# Create your models here.

def get_datetime_now():
    return timezone.now() + timedelta(minutes=3)


class User(AbstractUser):
    mobile = models.CharField(max_length=11, null=True)


class OtpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    mobile = models.CharField(max_length=11)
    otp_code = models.CharField(max_length=5)

    valid_from = models.DateTimeField(default=django.utils.timezone.now, null=True)
    valid_until = models.DateTimeField(default=get_datetime_now, null=True)
