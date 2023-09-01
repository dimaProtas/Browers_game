from django.db.models import Count
from django.core.cache import cache

from .models import *

menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "Игра", 'url_name': 'game'},
        {'title': "Профиль", 'url_name': 'profile'},
        {'title': "Таблица лидеров", 'url_name': 'top'},
        {'title': "Вход", 'url_name': 'login'},
        {'title': "Регистрация", 'url_name': 'register'},
        ]


class DataMixin:
    paginate_by = 30
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(4)
        context['menu'] = user_menu
        return context