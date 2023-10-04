from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


# Модель юзера
class CustomUser(AbstractUser):
    username = models.CharField(max_length=250, unique=True)
    status = models.CharField(max_length=30, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True, verbose_name='about_me')
    email = models.EmailField(('email address'), unique=True)
    vk = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', blank=True, verbose_name='avatar')
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацтю')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username


# Модель профиля игрока, то есть можем вести некую статистику и выводить ее на условной таблице лидеров
class ProfileUser(models.Model):
    user_name = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile_user')
    top_result = models.IntegerField(default=0)
    count_game = models.IntegerField(default=0)

    def __str__(self):
        return self.user_name.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class DuckHuntModel(models.Model):
    best_result = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    profile_user = models.OneToOneField(ProfileUser, on_delete=models.PROTECT, related_name='duck_hunt')

    class Meta:
        verbose_name = 'Duck Hunt'
        verbose_name_plural = 'Duck Hunt'


class SuperMarioModel(models.Model):
    best_result = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    profile_user = models.OneToOneField(ProfileUser, on_delete=models.PROTECT, related_name='super_mario')

    class Meta:
        verbose_name = 'Super Mario'
        verbose_name_plural = 'Super Mario'

class KerbyModel(models.Model):
    best_result = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    allies_saved = models.IntegerField(default=0)
    allies_lost = models.IntegerField(default=0)
    profile_user = models.OneToOneField(ProfileUser, on_delete=models.PROTECT, related_name='kerby')

    class Meta:
        verbose_name = 'Kerby'
        verbose_name_plural = 'Kerby'


class MessagesModel(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Сообщения'


class PostUser(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_post')
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='url')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='image/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title), allow_unicode=True).replace('-', '_')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class CommentModel(models.Model):
    post = models.ForeignKey(PostUser, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        ordering = ['-created_at']


class LikeModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUser, on_delete=models.CASCADE, related_name='like')

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

class DisLikeModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUser, on_delete=models.CASCADE, related_name='dis_like')

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Дизлай'
        verbose_name_plural = 'Дизлайки'


class FriendsRequest(models.Model):
    STATUS_CHOICE = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
    status = models.IntegerField(choices=STATUS_CHOICE, default=1)
    sent_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_sent")
    sent_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="request_received")
    sent_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sent_from', 'sent_to')
        verbose_name = 'Друзья'
        verbose_name_plural = 'Друзья'
