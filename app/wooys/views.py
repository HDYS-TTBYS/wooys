import json
import logging
import datetime


from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.utils import timezone

from accounts.models import CustomUser, UserIncluded
from accounts.forms import UserIncludedCreateForm

from .models import UploadImageByFile, Article, Like, Browsing, Comment
from .forms import ArticleCreateForm, ArticleCommentCreateForm

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
            # 検索文字列あり
            if s_word == "like":
                # 総合いいね順
                articles = Article.objects.filter(
                    is_release=True).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_like=Count('like')).order_by('-num_like')
            elif s_word == "weekLike":
                # 週間いいね順
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    is_release=True).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_like=Count('like', filter=Q(
                            like__created_at__gte=seven_days_ago))).order_by('-num_like')
            elif s_word == "browse":
                # 総合閲覧数順
                articles = Article.objects.filter(
                    is_release=True).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_browse=Count('browsing')).order_by('-num_browse')
            elif s_word == "weekBrowse":
                # 週間閲覧数順
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    is_release=True).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_browse=Count('browsing', filter=Q(
                            like__created_at__gte=seven_days_ago))).order_by('-num_browse')
            else:
                articles = Article.objects.filter(
                    is_release=True).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).order_by("-created_at")
        else:
            # 検索文字列なし
            if s_word == "like":
                # 総合いいね数
                articles = Article.objects.filter(
                    is_release=True).annotate(num_like=Count('like')).order_by('-num_like')
            elif s_word == "weekLike":
                # 週間いいね数
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    is_release=True).annotate(num_like=Count('like', filter=Q(
                        like__created_at__gte=seven_days_ago))).order_by('-num_like')
            elif s_word == "browse":
                # 総合閲覧数
                articles = Article.objects.filter(
                    is_release=True).annotate(
                    num_browse=Count('browsing')).order_by('-num_browse')
            elif s_word == "weekBrowse":
                # 週間閲覧数
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    is_release=True).annotate(num_browse=Count('browsing', filter=Q(
                        like__created_at__gte=seven_days_ago))).order_by('-num_browse')
            else:
                articles = Article.objects.filter(
                    is_release=True).order_by("-created_at")
        return articles


class ArticleCreateView(LoginRequiredMixin, generic.CreateView):
    """記事作成ページ"""
    model = Article
    template_name = "wooys/create.html"
    form_class = ArticleCreateForm
    success_url = reverse_lazy("wooys:index")

    def form_valid(self, form):
        article = form.save(commit=False)
        article.user = self.request.user
        article.save()
        messages.success(self.request, "記事を作成しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "記事の作成に失敗しました。")


class ArticleDetailView(generic.DetailView):
    """記事詳細ページ"""
    model = Article
    template_name = "wooys/detail.html"

    def get_context_data(self, **kwargs):
        """閲覧履歴を記録"""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        article.browsing_set.create()
        return context


class ArticleUpdateView(LoginRequiredMixin, generic.UpdateView):
    """記事アップデートページ"""
    model = Article
    template_name = "wooys/update.html"
    form_class = ArticleCreateForm

    def get_success_url(self):
        return reverse_lazy("wooys:mypage")

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
        q_word = self.request.GET.get('query')
        if q_word is not None:
            q_word.split()
        s_word = self.request.GET.get('sort')
        # リクエストしたユーザーが作成した記事のみ
        if q_word:
            # 検索文字列あり
            if s_word == "like":
                # 総合いいね順
                articles = Article.objects.filter(
                    user=self.request.user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_like=Count('like')).order_by('-num_like')
            elif s_word == "weekLike":
                # 週間いいね順
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    user=self.request.user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_like=Count('like', filter=Q(
                            like__created_at__gte=seven_days_ago))).order_by('-num_like')
            elif s_word == "browse":
                # 総合閲覧数順
                articles = Article.objects.filter(
                    user=self.request.user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_browse=Count('browsing')).order_by('-num_browse')
            elif s_word == "weekBrowse":
                # 週間閲覧数順
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    user=self.request.user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).annotate(
                        num_browse=Count('browsing', filter=Q(
                            like__created_at__gte=seven_days_ago))).order_by('-num_browse')
            else:
                articles = Article.objects.filter(
                    user=self.request.user).filter(
                    Q(title__in=q_word) | Q(search_tag__in=q_word)).order_by("-created_at")
        else:
            # 検索文字列なし
            if s_word == "like":
                # 総合いいね数
                articles = Article.objects.filter(
                    user=self.request.user).annotate(
                    num_like=Count('like')).order_by('-num_like')
            elif s_word == "weekLike":
                # 週間いいね数
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    user=self.request.user).annotate(
                    num_like=Count('like', filter=Q(
                        like__created_at__gte=seven_days_ago))).order_by('-num_like')
            elif s_word == "browse":
                # 総合閲覧数
                articles = Article.objects.filter(
                    user=self.request.user).annotate(
                    num_browse=Count('browsing')).order_by('-num_browse')
            elif s_word == "weekBrowse":
                # 週間閲覧数
                seven_days_ago = timezone.now() - datetime.timedelta(days=7)
                articles = Article.objects.filter(
                    user=self.request.user).annotate(
                    num_browse=Count('browsing', filter=Q(
                        like__created_at__gte=seven_days_ago))).order_by('-num_browse')
            else:
                articles = Article.objects.filter(
                    user=self.request.user).order_by("-created_at")
        return articles


@ require_POST
@ csrf_exempt
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
        # URLをjsonとして返す。
        return json_response
    except ValueError:
        response = {
            "data": ""
        }
        json_response = JsonResponse(response)
        # URLをjsonとして返す。
        return json_response


@ csrf_exempt
def Goodfunc(request, *args, **kwargs):
    """いいね機能
    POST
    {
        user_id: "",
        article_id: "",
    }
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        user_id = body["user_id"]
        article_id = body["article_id"]
        is_user = CustomUser.objects.filter(
            pk=user_id)
        # userの存在確認
        if is_user.count():
            # いいね済か？
            is_like = Like.objects.filter(
                user_id=user_id).filter(article_id=article_id)
            if is_like.count():
                is_like.delete()
                response = {"response": "deleted"}
                return JsonResponse(response)
            else:
                article = Article.objects.get(pk=article_id)
                article.like_set.create(user_id=user_id)
                response = {"response": "created"}
                return JsonResponse(response)
        else:
            response = {"response": "no_user"}
            return JsonResponse(response)

    if request.method == 'GET':
        article_id = request.GET.get('article_id')
        user_id = request.GET.get('user_id')
        if user_id != "undefined":
            is_good = Like.objects.filter(
                user_id=user_id).filter(article_id=article_id).count()
        else:
            is_good = 0
        good_num = Like.objects.filter(article_id=article_id).count()
        response = {
            "user_id": user_id,
            "is_good": is_good,
            "good_num": good_num,
        }
        return JsonResponse(response)


class ThumbnailCreateView(LoginRequiredMixin, generic.CreateView):
    """サムネイル登録ページ"""
    model = UserIncluded
    template_name = "wooys/thumbnail.html"
    form_class = UserIncludedCreateForm
    success_url = reverse_lazy("wooys:index")

    def form_valid(self, form):
        user_included = form.save(commit=False)
        user_included.user = self.request.user
        user_included.save()
        messages.success(self.request, "サムネイルの登録に成功しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "サムネイルの登録に失敗しました。")


class ThumbnailUpdateView(LoginRequiredMixin, generic.UpdateView):
    """サムネイル更新ページ"""
    model = UserIncluded
    template_name = "wooys/thumbnail.html"
    form_class = UserIncludedCreateForm

    def get_success_url(self):
        return reverse_lazy("wooys:mypage")

    def form_valid(self, form):
        request_user = self.request.user
        user_included = UserIncluded.objects.filter(pk=self.kwargs['pk'])
        is_update = user_included.user = request_user
        if is_update:
            messages.success(self.request, "サムネイルを更新しました。")
            return super().form_valid(form)
        else:
            messages.warning(self.request, "サムネイルを更新する権限がありません。")
            return redirect("wooys:index")

    def form_invalid(self, form):
        messages.error(self.request, "サムネイルの更新に失敗しました。")
        return super().form_invalid(form)


class ArticleCommentCreateView(LoginRequiredMixin, generic.CreateView):
    """記事コメント作成ページ"""
    model = Comment
    template_name = "wooys/create_comment.html"
    form_class = ArticleCommentCreateForm

    def get_success_url(self):
        return reverse('wooys:detail', kwargs={'pk': self.object.article.id})

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        article_pk = self.kwargs['pk']
        article = Article.objects.get(pk=article_pk)
        comment.article = article
        comment.save()
        messages.success(self.request, "コメントを作成しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "コメントの作成に失敗しました。")


class ArticleCommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    """記事コメントアップデートページ"""
    model = Comment
    template_name = "wooys/update_comment.html"
    form_class = ArticleCommentCreateForm

    def get_success_url(self):
        return reverse('wooys:detail', kwargs={'pk': self.object.article.id})

    def form_valid(self, form):
        request_user = self.request.user
        comment = Comment.objects.filter(pk=self.kwargs['pk'])
        is_update = comment.user = request_user
        if is_update:
            messages.success(self.request, "記事コメントを更新しました。")
            return super().form_valid(form)
        else:
            messages.warning(self.request, "記事コメントを更新する権限がありません。")
            return redirect("wooys:index")

    def form_invalid(self, form):
        messages.error(self.request, "記事の更新に失敗しました。")
        return super().form_invalid(form)
