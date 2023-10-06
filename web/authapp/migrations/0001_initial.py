# Generated by Django 4.2.4 on 2023-10-06 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=250, unique=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('about_me', models.TextField(blank=True, null=True, verbose_name='about_me')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('vk', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('github', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar', models.ImageField(blank=True, upload_to='avatar/%Y/%m/%d/', verbose_name='avatar')),
                ('is_activated', models.BooleanField(db_index=True, default=True, verbose_name='Прошел активацтю')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_result', models.IntegerField(default=0)),
                ('count_game', models.IntegerField(default=0)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='SuperMarioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_result', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='super_mario', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Super Mario',
                'verbose_name_plural': 'Super Mario',
            },
        ),
        migrations.CreateModel(
            name='PostUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='url')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, upload_to='image/%Y/%m/%d/', verbose_name='Изображение')),
                ('views', models.IntegerField(default=0, verbose_name='Кол-во просмотров')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MessagesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='KerbyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_result', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('allies_saved', models.IntegerField(default=0)),
                ('allies_lost', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kerby', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Kerby',
                'verbose_name_plural': 'Kerby',
            },
        ),
        migrations.CreateModel(
            name='DuckHuntModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('best_result', models.IntegerField(default=0)),
                ('total_points', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='duck_hunt', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Duck Hunt',
                'verbose_name_plural': 'Duck Hunt',
            },
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='authapp.postuser')),
            ],
            options={
                'verbose_name': 'Коментарий',
                'verbose_name_plural': 'Коментарии',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BombermanModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_win', models.IntegerField(default=0)),
                ('total_kills', models.IntegerField(default=0)),
                ('kill_npc_best', models.IntegerField(default=0)),
                ('profile_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bomberman', to='authapp.profileuser')),
            ],
            options={
                'verbose_name': 'Bomberman',
                'verbose_name_plural': 'Bomberman',
            },
        ),
        migrations.CreateModel(
            name='LikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='authapp.postuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Лайк',
                'verbose_name_plural': 'Лайки',
                'unique_together': {('user', 'post')},
            },
        ),
        migrations.CreateModel(
            name='FriendsRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Rejected')], default=1)),
                ('sent_on', models.DateTimeField(auto_now=True)),
                ('sent_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_sent', to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Друзья',
                'verbose_name_plural': 'Друзья',
                'unique_together': {('sent_from', 'sent_to')},
            },
        ),
        migrations.CreateModel(
            name='DisLikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dis_like', to='authapp.postuser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Дизлай',
                'verbose_name_plural': 'Дизлайки',
                'unique_together': {('user', 'post')},
            },
        ),
    ]
