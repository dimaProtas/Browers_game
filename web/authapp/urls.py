from django.urls import path
from authapp import views, consumers


urlpatterns = [
    path('game/', views.game, name='game'),
    path('game/doom_game/', views.start_game, name='start_game'),
]


