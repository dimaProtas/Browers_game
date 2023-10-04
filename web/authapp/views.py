from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.paginator import Paginator
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm, MessageForm, PostForm
from authapp.models import ProfileUser, CustomUser, MessagesModel, PostUser, CommentModel, LikeModel, DisLikeModel, \
    FriendsRequest, DuckHuntModel, SuperMarioModel, KerbyModel
from authapp.utils import DataMixin
from django.views.generic import DetailView
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify
from django.db.models import Count
from django.utils import timezone
import locale
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json
from django.core.signing import BadSignature
from .utilites import signer



# Функция проверки отношений между пользователями.
def get_relationship_status(user1, user2):
    # Проверяем, есть ли запрос в друзья от пользователя user1 к пользователю user2
    friend_request = FriendsRequest.objects.filter(
        sent_from=user1,
        sent_to=user2,
        status=1  # Статус "Pending" означает, что запрос в друзья ожидает подтверждения
    ).first()

    if friend_request:
        return "request_sent"  # Запрос в друзья уже отправлен
    elif FriendsRequest.objects.filter(
        (Q(sent_from=user1, sent_to=user2, status=2) | Q(sent_from=user2, sent_to=user1, status=2))
    ).exists():
        return "friend"  # Пользователи уже друзья
    else:
        return "not_friends"  # Пользователи не являются друзьями и нет активных запросов


def users_all_view(request):
    users = CustomUser.objects.annotate(post_count=Count('user_post')).exclude(id=request.user.id)
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Обновляем объекты CustomUser с атрибутом status
    for user in page_obj:
        user.relationship_statuses = get_relationship_status(request.user, user)

    return render(request, 'users.html', {'page_obj': page_obj})

class MessageView(View):
    def get(self, request):
        current_user = request.user
        print(current_user)
        messages = MessagesModel.objects.all()
        form = MessageForm()

        if messages.count() > 20:
            # Если количество записей больше 20, удаляем лишние записи
            messages_to_delete = messages.order_by('created_at')[:messages.count() - 20]
            for message in messages_to_delete:
                message.delete()

        return render(request, 'game/pygbag.html', {'messages': messages, 'current_user': current_user, 'form': form})


def tank(request):
    return render(request, 'game/tank.html')


class KerbyView(View):
    def get(self, request):
        current_user = request.user
        messages = MessagesModel.objects.all()
        form = MessageForm()

        if messages.count() > 20:
            # Если количество записей больше 20, удаляем лишние записи
            messages_to_delete = messages.order_by('created_at')[:messages.count() - 20]
            for message in messages_to_delete:
                message.delete()

        return render(request, 'game/kirby.html', {'messages': messages, 'current_user': current_user, 'form': form})

class SuperMarioViews(View):
    def get(self, request):
        current_user = request.user
        messages = MessagesModel.objects.all()
        form = MessageForm()

        if messages.count() > 20:
            # Если количество записей больше 20, удаляем лишние записи
            messages_to_delete = messages.order_by('created_at')[:messages.count() - 20]
            for message in messages_to_delete:
                message.delete()

        return render(request, 'game/mario_js.html', {'messages': messages, 'current_user': current_user, 'form': form})


class DuckHuntViews(View):
    def get(self, request):
        current_user = request.user
        print(current_user)
        messages = MessagesModel.objects.all()
        form = MessageForm()

        if messages.count() > 20:
            # Если количество записей больше 20, удаляем лишние записи
            messages_to_delete = messages.order_by('created_at')[:messages.count() - 20]
            for message in messages_to_delete:
                message.delete()

        return render(request, 'game/duck_hunt.html', {'messages': messages, 'current_user': current_user, 'form': form})


def game_js(request):
    return render(request, 'index_game.html')


def start_game(request):
    # logger.info("start_game view called")
    # game_process = multiprocessing.Process(target=run_game_and_send_data)
    # game_process.start()

    # return render(request, 'index_game.html')
    return render(request, 'game_stream.html')


def game(request):
    return render(request, 'game.html')


def home(request):
    # distinct=True - позволяет подсчитывать только уникальные элементы
    post = PostUser.objects.annotate(comment_count=Count('comments')).annotate(
        like_count=Count('like', distinct=True)).annotate(
        dis_like_count=Count('dis_like', distinct=True)).order_by('-created_at')
    paginator = Paginator(post, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})


class PostCreated(CreateView):
    model = PostUser
    form_class = PostForm
    template_name = 'add_post_form.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = PostUser
    fields = ['title', 'text', 'image']
    template_name = 'edit_post.html'
    success_url = '/profile/'


class PostDetailView(DetailView):
    model = PostUser
    template_name = 'detail_post.html'
    context_object_name = 'detail_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        # Добавляем количество лайков в контекст
        context['like_count'] = LikeModel.objects.filter(post=self.object).count()
        context['dislike_count'] = DisLikeModel.objects.filter(post=self.object).count()
        context['comment_count'] = CommentModel.objects.filter(post=self.object).count()
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(CustomUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def profile_user_view(request):
    user_id = request.user.id
    friends = FriendsRequest.objects.filter(
        Q(sent_from=user_id, status=2) | Q(sent_to=user_id, status=2)
    ).order_by('-sent_on')
    friends_count = friends.count()
    request_friends = FriendsRequest.objects.filter(sent_to=user_id, status=1)
    request_friends_count = request_friends.count()
    post_user = PostUser.objects.filter(author_id=user_id)
    profile = ProfileUser.objects.get(user_name_id=user_id)
    user = CustomUser.objects.get(id=profile.user_name_id)
    return render(request, 'profile.html', {'profile': profile, 'user': user, 'post_user': post_user,
                                            'friends': friends, 'request_friends': request_friends,
                                            'request_friends_count': request_friends_count, 'friends_count': friends_count})


class ProfileDetailUserView(DetailView):
    model = CustomUser
    template_name = 'detail_profile_user.html'
    context_object_name = 'detail_profile_user'


def delete_post(request, post_id):
    try:
        post = PostUser.objects.get(id=post_id)
        post.delete()
        return JsonResponse({'sucses': True})
    except PostUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)


def delete_comment(request, comment_id):
    try:
        comment = CommentModel.objects.get(id=comment_id)
        comment.delete()
        return JsonResponse({'sucses': True})
    except CommentModel.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comment not found'}, status=404)


def top_players(request):
    top = ProfileUser.objects.annotate(post_count=Count('user_name__user_post')).order_by('-top_result')[:10]
    return render(request, 'top.html', {'top': top})

class GameResultDetail(DetailView):
    model = ProfileUser
    template_name = 'game_progress_detail.html'
    context_object_name = 'game_progress'


def logout_user(request):
    logout(request)
    return redirect('home')


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = CustomUserChangeForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = CustomUserChangeForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')


def toggle_like(request, post_id):
    post = get_object_or_404(PostUser, id=post_id)
    user = request.user

    like, create = LikeModel.objects.get_or_create(post=post, user=user)

    if create:
        like.save()
        message = 'like_add'
    else:
        like.delete()
        message = 'like_delete'

    return JsonResponse({'message': message})


def toggle_dis_like(request, post_id):
    post = get_object_or_404(PostUser, id=post_id)
    user = request.user

    dis_like, create = DisLikeModel.objects.get_or_create(post=post, user=user)

    if create:
        dis_like.save()
        message = 'dislike_add'
    else:
        dis_like.delete()
        message = 'dislike_delete'

    return JsonResponse({'message': message})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import PostUser


def add_comment(request, post_id):
    post = get_object_or_404(PostUser, id=post_id)
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    formatted_datetime = timezone.localtime(timezone.now()).strftime('%d %B %Y г. %H:%M')
    locale.setlocale(locale.LC_TIME, '')

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '')

        if comment_text:
            comment = CommentModel(
                author=request.user,
                post=post,
                content=comment_text
            )
            comment.save()

            return JsonResponse({'result': 'Success', 'author': request.user.username, 'content': comment_text,
                                 'created_at': formatted_datetime, 'comment_id': comment.id})
        else:
            return JsonResponse({'result': 'Empty comment'}, status=400)

    return JsonResponse({'result': 'Method not allowed'}, status=405)


def request_friends(request, friends_id):
    friends = get_object_or_404(CustomUser, id=friends_id)

    existing_request = FriendsRequest.objects.filter(
        sent_from=request.user,
        sent_to=friends,
        status=1  # Проверяем только запросы со статусом "Pending"
    ).first()

    if existing_request: #проверка на существование такого запроса
        return JsonResponse({'result': 'Request already exists'})

    if request.method == 'POST':
        request_friends = FriendsRequest(
            sent_from=request.user,
            sent_to=friends,
        )
        request_friends.save()
        return JsonResponse({'result': 'Success'})
    else:
        return JsonResponse({'result': 'Method not allowed'}, status=405)


def delete_request_friend(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)
    request_friends = get_object_or_404(
        FriendsRequest.objects.filter(
            Q(sent_from=friend, sent_to=request.user) | Q(sent_to=friend, sent_from=request.user)
        )
    )
    request_friends.delete()
    return JsonResponse({'result': 'Success'})


def done_cancel_friends(request, friend_id, status):
    friend = get_object_or_404(CustomUser, id=friend_id)
    request_friends = get_object_or_404(FriendsRequest, sent_from=friend, sent_to=request.user)
    if status == 'done':
        request_friends.status = 2
        request_friends.save()
        return JsonResponse({'result': 'done'})
    elif status == 'cancel':
        request_friends.delete()
        return JsonResponse({'result': 'delete'})


def game_add_profile(request):
    profile_user = ProfileUser.objects.get(user_name=request.user)
    profile_user.count_game += 1
    profile_user.save()
    return JsonResponse({'result': 'Success'})


@login_required
def duck_hunt_points_save(request, results):
    profile_user = ProfileUser.objects.get(user_name=request.user)
    try:
        duck_hunt_model = DuckHuntModel.objects.get(profile_user=profile_user)
    except DuckHuntModel.DoesNotExist:
        duck_hunt_model = DuckHuntModel(profile_user=profile_user)

    try:
        results = int(results)  # Преобразуем результат в число, если это не так
        if results > duck_hunt_model.best_result:
            duck_hunt_model.best_result = results
        duck_hunt_model.total_points += 1
        duck_hunt_model.save()
        return JsonResponse({'result': 'Success'})
    except ValueError:
        return HttpResponseBadRequest({'error': 'Invalid results format'})
    except Exception as e:
        return HttpResponseBadRequest({'error': str(e)})


@login_required
def super_mario_points_save(request, results):
    profile_user = ProfileUser.objects.get(user_name=request.user)
    try:
        super_mario_model = SuperMarioModel.objects.get(profile_user=profile_user)
    except SuperMarioModel.DoesNotExist:
        super_mario_model = SuperMarioModel(profile_user=profile_user)

    try:
        results = int(results)
        if results > super_mario_model.best_result:
            super_mario_model.best_result = results
        super_mario_model.total_points += 50
        super_mario_model.save()
        return JsonResponse({'result': 'Success'})
    except ValueError:
        return HttpResponseBadRequest({'error': 'Invalid results format'})
    except Exception as e:
        return HttpResponseBadRequest({'error': str(e)})


@login_required
def kerby_points_save(request):
    profile_user = ProfileUser.objects.get(user_name=request.user)
    try:
        kerby_model = KerbyModel.objects.get(profile_user=profile_user)
    except KerbyModel.DoesNotExist:
        kerby_model = KerbyModel(profile_user=profile_user)

    total_points = int(request.POST.get('total_points'))
    alias_saved = int(request.POST.get('alias_saved'))
    alias_lost = int(request.POST.get('alias_lost'))

    if total_points is not None:
        try:
            if total_points > kerby_model.best_result:
                kerby_model.best_result = total_points
            kerby_model.allies_saved += alias_saved
            kerby_model.allies_lost += alias_lost
            kerby_model.total_points += total_points
            kerby_model.save()
            return JsonResponse({'result': 'Success'})
        except ValueError:
            return HttpResponseBadRequest({'error': 'Invalid results format'})
        except Exception as e:
            return HttpResponseBadRequest({'error': str(e)})