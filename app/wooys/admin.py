from django.contrib import admin

from .models import UploadImageByFile, Article

# Register your models here.

admin.site.register(UploadImageByFile)
admin.site.register(Article)
