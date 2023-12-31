from django.apps import AppConfig
from django.dispatch import Signal
from authapp.utilites import send_activation_notification


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    def ready(self):
        import authapp.signals       # импортируем сигналы


user_registered = Signal()  # Создаем сигнал здесь


def user_registered_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registered.connect(user_registered_dispatcher)

