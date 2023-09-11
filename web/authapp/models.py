from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone


# Модель юзера
class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# Модель профиля игрока, то есть можем вести некую статистику и выводить ее на условной таблице лидеров
class ProfileUser(models.Model):
    user_name = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    top_result = models.IntegerField(default=None)
    count_game = models.IntegerField(default=0)


class MessagesModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

