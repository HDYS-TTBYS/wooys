# Generated by Django 2.2.12 on 2020-06-24 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wooys', '0002_auto_20200624_1959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='browse_num',
        ),
        migrations.RemoveField(
            model_name='article',
            name='like_num',
        ),
    ]
