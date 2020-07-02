from django.contrib import admin

from .models import UploadImageByFile, Article, Like, Browsing, Comment

# Register your models here.

admin.site.register(UploadImageByFile)
admin.site.register(Article)
admin.site.register(Like)
admin.site.register(Browsing)
admin.site.register(Comment)
