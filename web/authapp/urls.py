from django.urls import path


from authapp import views


urlpatterns = [
    path('pygbag/', views.MessageView.as_view(), name='pygbag'),
    path('game/', views.game, name='game'),
    path('game/doom_game/', views.start_game, name='start_game'),
    path('game/js_doom_game/', views.game_js, name='js_doom_game'),
    path('detail_post/<str:slug>', views.PostDetailView.as_view(), name='detail_post'),
    path('add_post/', views.PostCreated.as_view(), name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<str:slug>/', views.PostUpdateView.as_view(), name='edit_post'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('toggle_dislike/<int:post_id>/', views.toggle_dis_like, name='toggle_dis_like'),
]


