from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.core.paginator import Paginator
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm, MessageForm, PostForm
from authapp.models import ProfileUser, CustomUser, MessagesModel, PostUser
from authapp.utils import DataMixin
from django.views.generic import DetailView
from django.shortcuts import render
from django.db.models import F
from django.utils.text import slugify



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

def home(request):
    post = PostUser.objects.all()
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

class PostDetailView(DetailView):
    model = PostUser
    template_name = 'detail_post.html'
    context_object_name = 'detail_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
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
    profile = ProfileUser.objects.get(user_name_id=user_id)
    user = CustomUser.objects.get(id=profile.user_name_id)
    return render(request, 'profile.html', {'profile': profile, 'user': user})


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
