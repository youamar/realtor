from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    url_odoo = models.CharField(max_length=10)
    db_name = models.CharField(max_length=30)
    odoo_password = models.CharField(max_length=30)
    first_name = None
    last_name = None
    email = None