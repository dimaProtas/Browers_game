from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import ProfileUser, FriendsRequest


@receiver(pre_save, sender=FriendsRequest)
def update_sent_on(sender, instance, **kwargs):
    # Обновляем поле sent_on при каждом сохранении записи
    instance.sent_on = timezone.now()


# Сигналы для создания модели Profile при регистрации нового пользовател.
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user_name=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile_user.save()
