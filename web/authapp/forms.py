from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django import forms
from authapp.apps import user_registered
from .models import CustomUser, PostUser, CommentModel


# class CustomUserCreationForm(UserCreationForm):
#     username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#     password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
#
#     class Meta(UserCreationForm):
#         model = CustomUser
#         fields = ('email', 'username')
#
#
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'status', 'about_me', 'email', 'vk', 'instagram', 'github', 'avatar')


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(CustomUserCreationForm, instance=user)
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class MessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Введите ваше сообщение...'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = PostUser
        fields = ['title', 'text', 'image']

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=forms.FileInput(attrs={'class': 'image-input'}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Получаем пользователя из аргументов
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        if commit:
            instance.save()
        return instance


