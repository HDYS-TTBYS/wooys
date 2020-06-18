from django.urls import path
from . import views


app_name = "wooys"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", views.ArticleCreateView.as_view(), name="create"),
    path("detail/<int:pk>/",
         views.ArticleDetailView.as_view(), name="detail"),
    path("update/<int:pk>/",
         views.ArticleUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/",
         views.ArticleDeleteView.as_view(), name="delete"),
    path("good/", views.Good, name="good"),
    path("mypage/", views.MyPageView.as_view(), name="mypage"),
    path("uploadByFile/", views.UploadByFile, name="uploadByFile"),

]
