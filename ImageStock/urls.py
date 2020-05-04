"""ImageStock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

import settings

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
  path(r'swagger-docs/', schema_view),
  path('', include('apps.image_searching.urls')),
  path('admin/', admin.site.urls),
  path('account/', include('apps.myauth.urls')),
  path('account/author/', include('apps.author_profile.urls')),
  path('account/author/', include('apps.subscription_handling.urls')),
  path('account/consumer/', include('apps.consumer_profile.urls')),
  path('boards/', include('apps.board_handling.urls')),
  path('image/', include('apps.image_handling.urls')),
  path('collection/', include('apps.collection_handling.urls')),
  path('purchases/', include('apps.purchase_handling.urls')),
  path('api/', include('apps.collection_api_handling.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
