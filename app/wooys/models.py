from django.db import models

# Create your models here.


class UploadImageByFile(models.Model):
    """イメージアップロードモデル"""
    img = models.ImageField(upload_to="mediafiles", null=True)

    class Meta:
        verbose_name_plural = "UploadImageByFile"

    def __str__(self):
        return self.img.url
