from django.urls import path


from authapp import views


urlpatterns = [
    path('pygbag/', views.MessageView.as_view(), name='pygbag'),
    path('game/', views.game, name='game'),
    path('game/doom_game/', views.start_game, name='start_game'),
    path('game/js_doom_game/', views.game_js, name='js_doom_game')
]


