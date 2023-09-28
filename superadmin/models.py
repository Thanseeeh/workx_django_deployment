from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, blank=True)
    image = models.ImageField(upload_to='category', blank=True, null=True)
    is_active = models.BooleanField(default=True)