from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta:
        verbose_name_plural = "CustomUser"


class UserIncluded(models.Model):
    """ユーザー付属モデル"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="mediafiles", null=True)

    class Meta:
        verbose_name_plural = "Thumbnail"

    def __str__(self):
        return self.img.url
