from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from .models import PrivateMessagesModel
from authapp.models import FriendsRequest, CustomUser


def private_message_view(request):
    user_id = request.user.id
    current_user = request.user
    friends = FriendsRequest.objects.filter(
        Q(sent_from=user_id, status=2) | Q(sent_to=user_id, status=2)
    ).order_by('-sent_on')
    return render(request, 'private_message.html', {'friends': friends, 'current_user': current_user})


def get_messages(request, friends_id):
    friend = get_object_or_404(CustomUser, id=friends_id)

    messages = PrivateMessagesModel.objects.filter(
        Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user)
    ).order_by('timestamp')

    message_list = []

    for message in messages:
        message_data = {
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%d %B %Y г. %H:%M'),
        }
        message_list.append(message_data)

    return JsonResponse({'messages': message_list})

