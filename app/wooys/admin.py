from django.contrib import admin

from .models import UploadImageByFile, Article, Like, Browsing

# Register your models here.

admin.site.register(UploadImageByFile)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Browsing)
