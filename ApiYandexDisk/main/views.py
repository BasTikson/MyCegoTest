from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse
import requests


class GetApiResponse(View):
    template_name = 'main/UrlForm.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request,  *args, **kwargs):
        redirect_url = reverse('files')
        answer = {"status":"success", "url":redirect_url, "error": ""}
        url_yandex = request.POST.get('url_yandex')
        # Функция, котора будет стучаться по Yandex-му api и проверять на доступность и наличие файлов


        return JsonResponse(answer)

class Test(View):
    template_name = 'main/ViewsFiles.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request,  *args, **kwargs):
        answer={}
        return JsonResponse(answer)






# def fetch_yandex_api_sync(api_url, api_key, params=None):
#     headers = {
#         'Authorization': f'OAuth {api_key}',
#         'Accept': 'application/json'
#     }
#
#     try:
#         response = requests.get(api_url, headers=headers, params=params)
#         response.raise_for_status()  # Проверка на ошибки HTTP
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе к API Яндекса: {e}")
#         return None
#
# # Пример использования
# api_url = 'https://api.example.com/endpoint'
# api_key = 'your_api_key_here'
# params = {'param1': 'value1', 'param2': 'value2'}
#
# result = fetch_yandex_api_sync(api_url, api_key, params)
# if result:
#     print(result)