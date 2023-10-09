import json

from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView, UpdateView, ListView, DetailView, CreateView)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users_messages_app.models import Chat
from authapp.models import CustomUser
from django.http import JsonResponse


class MyChatsView(LoginRequiredMixin, ListView):
    model = Chat
    paginate_by = 10
    context_object_name = 'chats'
    template_name = 'my_chats.html'

    def get_queryset(self):
        return Chat.objects.filter(users=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class ChatView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat_detail.html'



class CreateChatView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        data = request.POST
        try:
            initiator = request.user
            companion = CustomUser.objects.get(id=int(data.get('companion')))

            if Chat.objects.get(users=(initiator.id, companion.id)):#проверка существования чата
                raise ValueError

            chat_inst = Chat.objects.create()
            chat_inst.users.add(initiator, companion)
            operation_result = 'ok'


        except (CustomUser.DoesNotExist, ValueError) as error:
            print(f'CreateChatView error === {error}')
            operation_result = 'error'

        return JsonResponse({'chat_status': operation_result})

@login_required
def send_message(request, *args, **kwargs):
    '''
    Функция получения сообщения с фронта
    :param request:
    :param args:
    :param kwargs:
    :return:
    '''
    return JsonResponse({'mess_status': 'ok'})

# class CreateChatView(LoginRequiredMixin, CreateView):
#     model = Chat
#     fields = ['users']
#     template_name = 'my_chats.html'