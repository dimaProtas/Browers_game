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

class DisLikeModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUser, on_delete=models.CASCADE, related_name='dis_like')

    class Meta:
        unique_together = ('user', 'post')