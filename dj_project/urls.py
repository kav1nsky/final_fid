
"""dj_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView, CreateView
from reg.views import reg_user, login_user, exit

urlpatterns = [
  path('admin', admin.site.urls),
  path('api/', include('api.urls')),
  path('', include('main.urls')),
  path('reg', reg_user, name='register'),
  path('login', login_user, name='login'),
  path('logout', exit, name='logout'),
  re_path('.*', TemplateView.as_view(template_name='index.html')),
  path('create_review', CreateView.as_view()),
]

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()