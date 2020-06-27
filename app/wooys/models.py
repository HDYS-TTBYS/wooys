from datetime import datetime

from django.db import models

from accounts.models import CustomUser

# Create your models here.


class UploadImageByFile(models.Model):
    """イメージアップロードモデル"""
    img = models.ImageField(upload_to="mediafiles", null=True)

    class Meta:
        verbose_name_plural = "UploadImageByFile"

    def __str__(self):
        return self.img.url


class Article(models.Model):
    """記事モデル"""
    user = models.ForeignKey(
        CustomUser, verbose_name="ユーザー", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="タイトル 40文字以内", max_length=40)
    search_tag = models.CharField(
        verbose_name="検索タグ (100文字以内空白区切りで入力してください)", max_length=100)
    content = models.TextField(verbose_name="本文", blank=True, null=True)
    is_release = models.BooleanField(verbose_name='公開する', default=False)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        verbose_name_plural = "Article"

    def get_like_num(self):
        if self.like_set.count():
            return self.like_set.count()
        else:
            return 0

    def get_browse_num(self):
        if self.browsing_set.count():
            return self.browsing_set.count()
        else:
            return 0

    def get_comment_num(self):
        if self.comment_set.count():
            return self.comment_set.count()
        else:
            return 0

    def get_comment(self):
        if self.comment_set.all():
            return self.comment_set.all()
        else:
            return 0

    def __str__(self):
        return self.title


class Comment(models.Model):
    """記事コメントモデル"""
    article = models.ForeignKey(
        'Article', verbose_name="記事", on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, verbose_name="ユーザー", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="タイトル 40文字以内", max_length=40)
    content = models.TextField(verbose_name="本文", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)


class Like(models.Model):
    """いいねモデル"""
    article = models.ForeignKey(
        'Article', verbose_name="記事", on_delete=models.CASCADE)
    user_id = models.IntegerField(
        verbose_name="ユーザー", default=0)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)


class Browsing(models.Model):
    """閲覧履歴モデル"""
    article = models.ForeignKey(
        'Article', verbose_name="記事", on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="閲覧日時", auto_now_add=True)
