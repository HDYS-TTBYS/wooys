from django.views import generic
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import UploadImageByFile

import logging

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
        logging.debug(response)
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


class UploadByUrl(generic.TemplateView):
    pass
