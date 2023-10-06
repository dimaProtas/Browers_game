from django.urls import path


from users_messages_app import views


urlpatterns = [

    path('chat_list/<str:slug>/', views.MyChatsView.as_view(), name='chat_list'),
    path('chat/<str:slug>/', views.ChatView.as_view(), name='chat'),
    path('chat/create_chat/<int:user_id>', views.CreateChatView.as_view(), name='create_chat'),


]


