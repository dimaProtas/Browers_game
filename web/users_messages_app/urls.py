from django.urls import path


from users_messages_app import views

app_name = 'users_messages_app'
urlpatterns = [
    path('private_message/', views.private_message_view, name='private_message'),
    path('get_messages/<int:friends_id>/', views.get_messages),
    # path('chat_list/<str:slug>/', views.MyChatsView.as_view(), name='chat_list'),
    # path('chat/<str:slug>/', views.ChatView.as_view(), name='chat'),
    # path('chat/create_chat/<int:user_id>', views.CreateChatView.as_view(), name='create_chat'),
]


