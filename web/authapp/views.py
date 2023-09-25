from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.core.paginator import Paginator
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm, MessageForm, PostForm
from authapp.models import ProfileUser, CustomUser, MessagesModel, PostUser, CommentModel, LikeModel, DisLikeModel
from authapp.utils import DataMixin
from django.views.generic import DetailView
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify
from django.db.models import Count
from django.utils import timezone
import locale
from django.http import JsonResponse


class MessageView(View):
    def get(self, request):
        curent_user = request.user
        print(curent_user)
        messages = MessagesModel.objects.all()
        form = MessageForm()

        if messages.count() > 20:
            # Если количество записей больше 20, удаляем лишние записи
            messages_to_delete = messages.order_by('created_at')[:messages.count() - 20]
            for message in messages_to_delete:
                message.delete()

        return render(request, 'pygbag.html', {'messages': messages, 'curent_user': curent_user, 'form': form})

    # def post(self, request):
    #     # Обработка создания нового сообщения
    #     if request.method == 'POST':
    #         form = MessageForm(request.POST)
    #         if form.is_valid():
    #
    #             sender = request.user
    #             message_text = form.cleaned_data['message']
    #             message = MessagesModel(sender=sender, message=message_text)
    #             message.save()
    #
    #             # return redirect('/pygbag')
    #
    #     messages = MessagesModel.objects.all()
    #     return render(request, 'pygbag.html', {'messages': messages, 'form': form})

    def delete(self, request, message_id):
        # Обработка удаления сообщения
        pass


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


import socket
from django.http import HttpResponse
from django.views.generic import View


class SocketServerView(View):
    def get(self, request):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 12345

        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        while True:
            data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
            print("received message: %s" % data)
            response = HttpResponse(f'{data}')
            sock.close()
            return response


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
    post_user = PostUser.objects.filter(author_id=user_id)
    profile = ProfileUser.objects.get(user_name_id=user_id)
    user = CustomUser.objects.get(id=profile.user_name_id)
    return render(request, 'profile.html', {'profile': profile, 'user': user, 'post_user': post_user})


def delete_post(request, post_id):
    try:
        post = PostUser.objects.get(id=post_id)
        post.delete()
        return JsonResponse({'sucses': True})
    except PostUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)


def top_players(request):
    top = ProfileUser.objects.order_by('-top_result')[:5]
    return render(request, 'top.html', {'top': top})


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
                                 'created_at': formatted_datetime})
        else:
            return JsonResponse({'result': 'Empty comment'}, status=400)

    return JsonResponse({'result': 'Method not allowed'}, status=405)
