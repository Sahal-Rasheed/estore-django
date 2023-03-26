from django.db import models

# Create your models here.

class Banner(models.Model):
    banner = models.ImageField(upload_to='banners',null=True,blank=True)
    is_live = models.BooleanField(default=False)