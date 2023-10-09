from django.urls import path


from users_messages_app import views

app_name = 'users_messages_app'
urlpatterns = [

    path('chat_list/', views.MyChatsView.as_view(), name='chat_list'),
    path('chat/create_chat/', views.CreateChatView.as_view(), name='create_chat'),
    path('chat/<str:slug>/', views.ChatView.as_view(), name='chat'),
    path('chat/send_mess/', views.send_message, name='send_mess'),

]


