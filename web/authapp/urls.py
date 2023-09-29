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
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit_post/<str:slug>/', views.PostUpdateView.as_view(), name='edit_post'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('toggle_dislike/<int:post_id>/', views.toggle_dis_like, name='toggle_dis_like'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('mario_js/', views.mario, name='mario'),
    path('duck_hunt/', views.DuckHuntViews.as_view(), name='duck_hunt'),
    path('detail_profile_user/<int:pk>/', views.ProfileDetailUserView.as_view(), name='detail_profile_user'),
    path('users_all/', views.users_all_view, name='users_all'),
    path('request_friends/<int:friends_id>/', views.request_friends),
    path('delete_request_friends/<int:friend_id>/', views.delete_request_friend),
    path('done_cancel_friend/<int:friend_id>/<str:status>/', views.done_cancel_friends),
    path('game_add_profile/', views.game_add_profile),
    path('duck_hunt_save_points/<int:results>/', views.duck_hunt_points_save),
]


