import json
import urllib.error
import urllib.request
import logging
import requests
import io
import os
import uuid

from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import UploadImageByFile, Article
from .forms import ArticleCreateForm

from django.conf import settings

# Create your views here.


class IndexView(generic.TemplateView):
    template_name = "wooys/index.html"


class CreateView(generic.TemplateView):
    template_name = "wooys/create.html"


@require_POST
@csrf_exempt
def UploadByFile(request):
    """/UploadByFile で呼び出される。"""
    # アップロードされたファイルを保存する。
    file = request.FILES['image']
    photo = UploadImageByFile(img=file)
    try:
        photo.save()
        # ファイルにアクセスするためのURLを作成する。
        download_url = "{0}://{1}{2}".format(request.scheme,
                                             request.get_host(), photo.img.url)
        response = {
            "success": 1,
            "file": {
                "url": download_url

            }
        }
        # URLをjsonとして返す。
        return JsonResponse(response)
    except ValueError:
        response = {
            "success": 0,
            "file": {
                "url": ""
            }
        }
        return JsonResponse(response)


@require_POST
@csrf_exempt
def UploadByUrl(request):
    """/UploadByUrl で呼び出される。"""
    # アップロードされたファイルを保存する。
    datas = json.loads(request.body)
    url = datas["url"]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            str_uuid = str(uuid.uuid4())
            img_path = settings.MEDIA_URL + str_uuid
            save_path = settings.MEDIA_ROOT + img_path
            print(save_path)
            with open(save_path, 'wb') as file:
                file.write(response.content)

            photo = UploadImageByFile(img=img_path)
            photo.save()

            # ファイルにアクセスするためのURLを作成する。
            download_url = "{0}://{1}{2}".format(request.scheme,
                                                 request.get_host(), photo.img.url)
            response = {
                "success": 1,
                "file": {
                    "url": download_url

                }
            }
            # URLをjsonとして返す。
            return JsonResponse(response)

    except urllib.error.URLError as e:
        response = {
            "success": 0,
            "file": {
                "url": ""
            }
        }
        return JsonResponse(response)


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    model = Article
    template_name = "wooys/create.html"
    form_class = ArticleCreateForm
    success_url = reverse_lazy("wooys:index")

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, "記事を作成しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "記事の作成に失敗しました。")
