from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ProfileUser, MessagesModel


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'top_result', 'count_game')
    list_display_links = ('user_name', 'top_result', 'count_game')
    search_fields = ('user_name',)


admin.site.register(ProfileUser, UserProfileAdmin)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message', 'created_at']
    list_display_links = ['id']
    search_fields = ['sender']


admin.site.register(MessagesModel, MessagesAdmin)
