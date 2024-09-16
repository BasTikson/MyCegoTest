from http.client import responses

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse
import requests
from django.http import FileResponse, Http404
from .yandexService import YandexDisk
import json
import os


class GetApiResponse(View):
    template_name = 'main/UrlForm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request,  *args, **kwargs):
        redirect_url = reverse('files')
        answer = {"status":"", "url":redirect_url, "error": ""}
        url_yandex = request.POST.get('url_yandex')
        ya = YandexDisk(url_yandex)
        check = ya.check_file_access()

        if check["status"] == "success":
            answer["status"] = "success"
            request.session['url_yandex'] = url_yandex
        else:
            answer["status"] = "error"
            answer["error"] = "Упс, кажется вы ввели не ту ссылку!"
        return JsonResponse(answer)

class Test(View):
    template_name = 'main/ViewsFiles.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request,  *args, **kwargs):
        action = request.POST["action"]
        answer = {}
        print("Post запрос пришел, action: ", action)
        if action == "update":
            public_key = request.session.get('url_yandex', None)
            if public_key:
                ya = YandexDisk(public_key)
                files = ya.get_all_files()
                list_file = []
                for file in files:
                    list_file.append({"name": file['name'], "path": file['path']})
                answer["status"] = "success"
                answer["files"] = list_file

                return JsonResponse(answer)

            else:
                print("Нет сохраненного диска")

        elif action == "downloadFiles":

            public_key = request.session.get('url_yandex', None)
            list_file = request.POST["listFiles"]
            if public_key and list_file:
                ya = YandexDisk(public_key)
                list_file = json.loads(list_file)
                for file in list_file:
                    file_path = ya.download_file(file)




                answer["status"] = "success"

                return JsonResponse(answer)

            else:
                answer["status"] = "error"
                answer["error"] = "Упс, не получилось скачать файлы!"
                return JsonResponse(answer)




        return JsonResponse(answer)















