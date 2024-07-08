from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import uuid




class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Categorie(models.Model):
    name = models.CharField(max_length=255)


class Rules(models.Model):
    ruleName = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, null=True, blank=True, on_delete=models.PROTECT)
    id_upload = models.CharField(max_length=255, default=uuid.uuid4)





