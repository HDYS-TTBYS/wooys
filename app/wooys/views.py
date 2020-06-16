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
from django.db.models import Q


from .models import UploadImageByFile, Article
from .forms import ArticleCreateForm

from django.conf import settings

# Create your views here.


# class IndexView(generic.TemplateView):
#     template_name = "wooys/index.html"


class IndexView(generic.ListView):
    """トップページ"""
    model = Article
    template_name = "wooys/index.html"
    paginate_by = 10

    def get_queryset(self):
        q_word = self.request.GET.get('query')
        if q_word is not None:
            q_word.split()
        s_word = self.request.GET.get('sort')

        if q_word:
            articles = Article.objects.filter(
                Q(title__in=q_word) | Q(search_tag__in=q_word))
        else:
            articles = Article.objects.all().order_by("-created_at")
        return articles


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    """記事作成ページ"""
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


class ArticleDetailView(generic.DetailView):
    """記事詳細ページ"""
    model = Article
    template_name = "wooys/detail.html"


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
            "data": download_url
        }
        json_response = JsonResponse(response)
        json_response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:5500'
        # URLをjsonとして返す。
        return json_response
    except ValueError:
        response = {
            "success": 0,
            "file": {
                "url": ""
            }
        }
        return ValueError


@ require_POST
@ csrf_exempt
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
