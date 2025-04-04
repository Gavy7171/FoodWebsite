""" 
URL configuration for Cooking_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings  # Added this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Recepies, name='Recepies'),
    path('recipes1/', include('recipes1.urls')),
    path('recipes2/', include('recipes2.urls')),
    path('recipes3/', include('recipes3.urls')),
    path('recipes4/', include('recipes4.urls')),
    path('recipes5/', include('recipes5.urls')),
    path('recipes6/', include('recipes6.urls')),
    path('recipes7/', include('recipes7.urls')),
    path('recipes8/', include('recipes8.urls')),
    path('recipes9/', include('recipes9.urls')),
    path('members/', include('members.urls')),
    path('recipes10/', include('recipes10.urls')),
]

# Add these lines to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)