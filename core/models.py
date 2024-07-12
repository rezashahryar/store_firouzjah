from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4

# Create your models here.


class User(AbstractUser):
    mobile = models.CharField(max_length=11, null=True)


class OtpRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    mobile = models.CharField(max_length=11)
    code = models.CharField(max_length=5)
