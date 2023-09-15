from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ProfileUser, MessagesModel, PostUser, CommentModel, LikeModel, DisLikeModel
from django.utils.safestring import mark_safe

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


class PostUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'author', 'get_text', 'created_at', 'get_photo', 'views']
    list_display_links = ['id']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['author']

    def get_text(self, obj):
        return obj.text[:20]

    get_text.short_description = "Пост"

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50">')
        else:
            return 'нет фото'

    get_photo.short_description = 'изображение'


admin.site.register(PostUser, PostUserAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'content', 'created_at']
    list_display_links = ['id']
    search_fields = ['post']


admin.site.register(CommentModel, CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    list_display = ['id', 'user', 'post']


admin.site.register(LikeModel, LikeAdmin)


class DisLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    list_display = ['id', 'user', 'post']


admin.site.register(DisLikeModel, DisLikeAdmin)
