from django.urls import path
from . import views


app_name = "wooys"
urlpatterns = [
    path("", views.IndexViews.as_view(), name="index"),
]
