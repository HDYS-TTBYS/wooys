from django.contrib import admin

from .models import CustomUser, UserIncluded

# Register your models here.


admin.site.register(CustomUser)
admin.site.register(UserIncluded)
