from rest_framework.routers import DefaultRouter
from .views import *
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('', index, name='index'),
]