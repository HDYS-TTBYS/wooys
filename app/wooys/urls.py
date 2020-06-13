from django.urls import path
from . import views


app_name = "wooys"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("uploadByFile/", views.UploadByFile, name="uploadByFile"),
    path("uploadByUrl/", views.UploadByUrl, name="uploadByUrl"),

]
