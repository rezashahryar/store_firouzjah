from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=11, null=True)


class OtpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    mobile = models.CharField(max_length=11)
    otp_code = models.CharField(max_length=5)

    valid_from = models.DateTimeField(default=timezone.now(), null=True)
    valid_until = models.DateTimeField(default=timezone.now() + timedelta(minutes=3), null=True)
