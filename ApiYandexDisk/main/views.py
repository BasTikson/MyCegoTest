import zipfile
from http.client import responses

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse
import requests
from django.http import FileResponse, Http404
from .yandexService import YandexDisk
import json
import os
import asyncio
import aiohttp


def check_existing_files(list_file, download_dir):
    """Проверка, какие файлы уже существуют в директории downloads."""
    existing_files = [file_name for file_name in list_file if os.path.exists(os.path.join(download_dir, file_name))]
    files_to_download = [file_name for file_name in list_file if file_name not in existing_files]
    return existing_files, files_to_download

def create_zip_response(files, download_dir):
    """Создание HTTP-ответа с ZIP-архивом."""
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'

    with zipfile.ZipFile(response, 'w') as zipf:
        for file_name in files:
            file_path = os.path.join(download_dir, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    zipf.writestr(file_name, f.read())
    return response




class GetApiResponse(View):
    template_name = 'main/UrlForm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        redirect_url = reverse('files')
        answer = {"status": "", "url": redirect_url, "error": ""}
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

    def post(self, request, *args, **kwargs):
        action = request.POST["action"]
        answer = {}

        if action == "update":

            public_key = request.session.get('url_yandex', None)
            if public_key:
                ya = YandexDisk(public_key)
                files = ya.get_all_files()
                list_file = [{"name": file['name'], "path": file['path']} for file in files]
                answer["status"] = "success"
                answer["files"] = list_file
                return JsonResponse(answer)
            else:
                answer["status"] = "error"
                answer["error"] = "Нет сохраненного диска"
                return JsonResponse(answer)


        elif action == "downloadFiles":
            public_key = request.session.get('url_yandex', None)
            list_file = request.POST.get("listFiles")
            download_dir = 'downloads'

            if public_key and list_file:
                list_file = json.loads(list_file)
                ya = YandexDisk(public_key)

                # Проверка, какие файлы уже существуют в директории downloads
                existing_files, files_to_download = check_existing_files(list_file, download_dir)

                if not files_to_download:
                    # Если все файлы уже существуют, возвращаем их сразу
                    return create_zip_response(existing_files, download_dir)
                else:
                    # Запуск асинхронной функции для скачивания файлов
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        results = loop.run_until_complete(ya.download_files(files_to_download))
                    finally:
                        loop.close()

                    if results:
                        # Объединяем скачанные файлы и существующие файлы
                        all_files = results + existing_files
                        return create_zip_response(all_files, download_dir)
                    else:
                        answer = {"status": "error", "error": "Упс, не получилось скачать файлы!"}
                        return JsonResponse(answer)
            else:
                answer = {"status": "error", "error": "Упс, не получилось скачать файлы!"}
                return JsonResponse(answer)


        return JsonResponse(answer)

