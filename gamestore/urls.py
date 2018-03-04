"""gamestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .views import frontpage
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('account/', include('gamestore.account.urls')),
    path('shop/', include('gamestore.shop.urls')),
    path('developer/', include('gamestore.developer.urls')),
    path('library/', include('gamestore.library.urls')),
    path('', frontpage),
    path('auth/', include('social_django.urls')),  # <- Here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

error404 = 'views.error404'
error500 = 'views.error500'
error403 = 'views.error403'
