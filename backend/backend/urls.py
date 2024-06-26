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
#  import os

#  from django.contrib import admin
from django.urls import path

from species_tree_backend.views import get_translations, get_childes_by_id, get_tree_by_id, get_tree_default, \
        get_favorites, search_by_words, get_tip_of_the_day, get_tip_of_the_day_by_id, check, \
        admin_try_login, admin_get_known_languages_all, admin_get_main_admin_language, \
        admin_get_tasks, admin_add_task, admin_edit_task, admin_delete_task, \
        admin_start_one_task, admin_stop_one_task, \
        admin_get_filling_stats, \
        admin_get_all_tips_translations, admin_add_tip, admin_edit_tip, admin_delete_tip, \
        admin_edit_tip_translation, admin_attach_tip_to_tree, admin_detach_tip_from_tree, admin_get_changed_tips, \
        admin_get_admin_users, admin_add_admin_user, admin_edit_admin_user, admin_delete_admin_user, \
        admin_get_count_1, admin_get_count_2, admin_get_count_3, \
        startup_start_tasks

from config import Config

urlpatterns = [
    # path('admin/', admin.site.urls),  # Стандартная админ-панель Django - просто не нужна
    path('api/get_translations', get_translations),
    path('api/get_childes_by_id/<int:_id>', get_childes_by_id),
    path('api/get_tree_by_id/<int:_id>', get_tree_by_id),
    path('api/get_tree_default', get_tree_default),
    path('api/get_favorites', get_favorites),
    path('api/search_by_words', search_by_words),
    path('api/get_tip_of_the_day', get_tip_of_the_day),
    path('api/get_tip_of_the_day_by_id/<int:_id>', get_tip_of_the_day_by_id),
    path('check', check),
    path('', check),
    # admin - общее
    path('api/admin_try_login', admin_try_login),
    path('api/admin_get_known_languages_all', admin_get_known_languages_all),
    path('api/admin_get_main_admin_language', admin_get_main_admin_language),
    # admin - задачи БД
    path('api/admin_get_tasks', admin_get_tasks),
    path('api/admin_add_task', admin_add_task),
    path('api/admin_edit_task', admin_edit_task),
    path('api/admin_delete_task', admin_delete_task),
    path('api/admin_start_one_task', admin_start_one_task),
    path('api/admin_stop_one_task', admin_stop_one_task),
    # admin - статистика заполнения
    path('api/admin_get_filling_stats', admin_get_filling_stats),
    # admin - перевод фактов
    path('api/admin_get_all_tips_translations', admin_get_all_tips_translations),
    path('api/admin_add_tip', admin_add_tip),
    path('api/admin_edit_tip', admin_edit_tip),
    path('api/admin_delete_tip', admin_delete_tip),
    path('api/admin_edit_tip_translation', admin_edit_tip_translation),
    path('api/admin_attach_tip_to_tree', admin_attach_tip_to_tree),
    path('api/admin_detach_tip_from_tree', admin_detach_tip_from_tree),
    path('api/admin_get_changed_tips', admin_get_changed_tips),
    # admin - управление админ-пользователями
    path('api/admin_get_admin_users', admin_get_admin_users),
    path('api/admin_add_admin_user', admin_add_admin_user),
    path('api/admin_edit_admin_user', admin_edit_admin_user),
    path('api/admin_delete_admin_user', admin_delete_admin_user),
    path(Config.BACKEND_ADMIN_PASSWORD + '/count_1', admin_get_count_1),
    path(Config.BACKEND_ADMIN_PASSWORD + '/count_2', admin_get_count_2),
    path(Config.BACKEND_ADMIN_PASSWORD + '/count_3', admin_get_count_3),
]

startup_start_tasks()
