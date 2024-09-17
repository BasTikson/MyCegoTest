from django.urls import path
from .views import *

urlpatterns = [
    path('', GetApiResponse.as_view(), name="main"),
    path('viewsFiles', Test.as_view(), name="files"),

]
