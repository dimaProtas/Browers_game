from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, ProfileUser, MessagesModel, PostUser, CommentModel, LikeModel, DisLikeModel, \
    FriendsRequest, DuckHuntModel, SuperMarioModel, KerbyModel, BombermanModel
from django.utils.safestring import mark_safe

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'username', 'email', 'get_avatar', 'is_staff', 'is_active', 'is_activated')
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('status', 'about_me', 'email', 'vk', 'instagram', 'github', 'avatar', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_activated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('id', 'username', 'status', 'about_me', 'email', 'vk', 'instagram', 'github', 'avatar', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('username',)

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="50">')
        else:
            return 'нет фото'

    get_avatar.short_description = 'Аватар'


admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'top_result', 'count_game')
    list_display_links = ('id', 'user_name', 'top_result', 'count_game')
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
    list_display_links = ['id']


admin.site.register(LikeModel, LikeAdmin)


class DisLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post']
    list_display_links = ['id']


admin.site.register(DisLikeModel, DisLikeAdmin)


class FriendsRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'sent_from', 'sent_to', 'sent_on']
    list_display_links = ['id']


admin.site.register(FriendsRequest, FriendsRequestAdmin)


class DuckHuntAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_user', 'best_result', 'total_points']
    list_display_links = ['id']


admin.site.register(DuckHuntModel, DuckHuntAdmin)


class SuperMarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_user', 'best_result', 'total_points']
    list_display_links = ['id']


admin.site.register(SuperMarioModel, SuperMarioAdmin)


class KerbyAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_user', 'best_result', 'total_points', 'allies_saved', 'allies_lost']
    list_display_links = ['id']


admin.site.register(KerbyModel, KerbyAdmin)


class BombermanAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile_user', 'count_win', 'total_kills', 'kill_npc_best']
    list_display_links = ['id']


admin.site.register(BombermanModel, BombermanAdmin)