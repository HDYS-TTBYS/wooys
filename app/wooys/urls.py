from django.urls import path
from . import views


app_name = "wooys"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("uploadByFile/", views.UploadByFile, name="uploadByFile"),
    path("uploadByUrl/", views.UploadByUrl.as_view(), name="uploadByUrl"),

]
