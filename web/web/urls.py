"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from authapp.models import DisLikeModel
from authapp.views import home, RegisterUser, LoginUser, profile_user_view, top_players, logout_user, \
    ProfileUpdateView, game, SocketServerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,  name='home'),

    path('trymore/', SocketServerView.as_view(), name='server'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', profile_user_view, name='profile'),
    path('top_players', top_players, name='top'),
    path('logout/', logout_user,  name='logout'),
    path('edit_profile/', ProfileUpdateView.as_view(),  name='edit_profile'),
    path('', include("authapp.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
