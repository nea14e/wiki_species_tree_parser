"""backend URL Configuration

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
import os

from django.contrib import admin
from django.urls import path

from species_tree_backend.views import get_childes_by_id, get_tree_by_id, get_tree_default, search_by_words, get_tip_of_the_day, check, \
        admin_get_count_1, admin_get_count_2, admin_get_count_3

from config import Config

urlpatterns = [
    # path('admin/', admin.site.urls),  # Стандартная админ-панель Django - просто не нужна
    path('api/get_childes_by_id/<int:_id>', get_childes_by_id),
    path('api/get_tree_by_id/<int:_id>', get_tree_by_id),
    path('api/get_tree_default', get_tree_default),
    path('api/search_by_words/<str:words>/<int:offset>', search_by_words),
    path('api/get_tip_of_the_day', get_tip_of_the_day),
    path('check', check),
    path('', check),
    path(Config.BACKEND_ADMIN_URL_PREFIX + '/count_1', admin_get_count_1),
    path(Config.BACKEND_ADMIN_URL_PREFIX + '/count_2', admin_get_count_2),
    path(Config.BACKEND_ADMIN_URL_PREFIX + '/count_3', admin_get_count_3),
]
