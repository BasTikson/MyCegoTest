from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import reverse


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