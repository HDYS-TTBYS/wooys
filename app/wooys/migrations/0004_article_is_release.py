# Generated by Django 2.2.12 on 2020-06-26 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wooys', '0003_auto_20200624_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_release',
            field=models.BooleanField(default=False, verbose_name='公開'),
        ),
    ]
