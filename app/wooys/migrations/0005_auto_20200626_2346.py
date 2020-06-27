# Generated by Django 2.2.12 on 2020-06-26 14:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wooys', '0004_article_is_release'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_release',
            field=models.BooleanField(default=False, verbose_name='公開する'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='タイトル 40文字以内')),
                ('content', models.TextField(blank=True, null=True, verbose_name='本文')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wooys.Article', verbose_name='記事')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ユーザー')),
            ],
        ),
    ]