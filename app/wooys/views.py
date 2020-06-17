import json
import logging

from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
    paginate_by = 3

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


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    """記事アップデートページ"""
    model = Article
    template_name = "wooys/update.html"
    form_class = ArticleCreateForm

    def get_success_url(self):
        return reverse_lazy("wooys:index")

    def form_valid(self, form):
        request_user = self.request.user
        article = Article.objects.filter(pk=self.kwargs['pk'])
        is_update = article.user = request_user
        if is_update:
            messages.success(self.request, "記事を更新しました。")
            return super().form_valid(form)
        else:
            messages.warning(self.request, "記事を更新する権限がありません。")
            return redirect("wooys:index")

    def form_invalid(self, form):
        messages.error(self.request, "記事の更新に失敗しました。")
        return super().form_invalid(form)


class ArticleDeleteView(LoginRequiredMixin, generic.DeleteView):
    """記事削除ページ"""
    model = Article
    template_name = "wooys/delete.html"
    success_url = reverse_lazy("wooys:index")

    def delete(self, request, *args, **kwargs):
        request_user = self.request.user
        is_delete = Article.objects.filter(user=request_user)
        if is_delete:
            messages.success(self.request, "記事を削除しました。")
            return super().delete(request, *args, **kwargs)
        else:
            messages.warning(self.request, "記事を削除する権限がありません。")
            return redirect("wooys:index")


class MyPageView(LoginRequiredMixin, generic.ListView):
    """マイページ"""
    model = Article
    template_name = "wooys/mypage.html"
    paginate_by = 3

    def get_queryset(self):
        request_user = self.request.user
        q_word = self.request.GET.get('query')
        s_word = self.request.GET.get('sort')
        if q_word is not None:
            q_word.split()
        if q_word:
            # リクエストしたユーザーが作成した記事を取得
            articles = Article.objects.filter(
                user=request_user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word))
        else:
            articles = Article.objects.filter(
                user=request_user).order_by("-created_at")
        return articles


@require_POST
@csrf_exempt
def UploadByFile(request):
    """/UploadByFile で呼び出される。 quillの画像アップロードAPI"""
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
