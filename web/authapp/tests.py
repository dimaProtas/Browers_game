from django.test import TestCase

from http import HTTPStatus
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from authapp.models import CustomUser, PostUser, LikeModel, DisLikeModel, CommentModel


# Create your tests here.


class TestMainPage(TestCase):
    """Тест для url - главная страница работает"""
    def test_page_open(self):
        path = reverse("home")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class StaticURLTests(TestCase):
    """Тесты для url - статичных адресов"""

    def setUp(self) -> None:
        self.guest_client = Client()

    def test_page_main(self) -> None:
        """Страница доступа по URL для ./web/urls"""

        pages: tuple = ('/', '', '/register/', '/login/')

        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_page_app(self) -> None:
        """Страница доступа по URL для ./authapp/urls"""

        pages: tuple = ('/pygbag/', '/game/', '/game/doom_game/', '/game/js_doom_game/', '/mario_js/', '/duck_hunt/',
                        '/users_all/')

        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_urls_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names: dict = {
            '': 'index.html',
            '/pygbag/': 'pygbag.html',
            '/register/': 'register.html',
            '/login/': 'login.html',
            '/game/': 'game.html',
            # '/top_players/': 'top.html',
            '/game/doom_game/': 'game_stream.html',
            '/game/js_doom_game/': 'index_game.html',
            '/mario_js/': 'mario_js.html',
            '/game/duck_hunt/': 'duck_hunt.html',
        }

        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                error_name: str = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)


class PostURLTests(TestCase):

    def setUp(self):

        self.guest_client = Client()  # неавторизованный пользователь

        self.user = CustomUser.objects.create_user(username='testik', password='testpassword', email='testik@mail.ru')
        self.authorized_client = Client() # авторизованный пользователь
        self.authorized_client.force_login(self.user)

        self.post = PostUser(author=self.user, title='Test Post', text='test text')
        self.post.save()
        self.like = LikeModel(user=self.user, post=self.post)
        self.dislike = DisLikeModel(user=self.user, post=self.post)
        self.comment = CommentModel(author=self.user, post=self.post, content='test comment', id=1)
        self.comment.save()

    def test_urls_guest_client(self):
        """Доступ неавторизованного пользователя к просмотру постов"""
        pages: tuple = ('/',
                        f'/detail_post/{str(self.post.slug)}',
                        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)


    def test_urls_authorized_client(self):
        """Доступ авторизованного пользователя"""
        pages: tuple = ('/',
                        f'/add_post/',
                        f'/game_add_profile/',
                        f'/edit_post/{self.post.slug}/',
                        f'/toggle_like/{self.post.id}/',
                        f'/toggle_dislike/{self.post.id}/',
                        f'/detail_profile_user/{self.user.id}/',
                        f'/duck_hunt_save_points/11/',

                        f'/delete_comment/{self.comment.id}/',
                        f'/delete_post/{self.post.id}/',

                        # f'/request_friends/{self.user.id}/', #  POST форма
                        # f'delete_request_friends/{self.user.id}/',
                        # f'/add_comment/{self.post.id}/', #  POST форма
                        )

        for page in pages:
            response = self.authorized_client.get(page)
            error_name = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)
