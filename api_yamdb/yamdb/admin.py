from django.contrib import admin

from .models import User, Title, Review, Comment
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username", "first_name", "last_name", "email", "bio", "role")
    search_fields = ("username",)
    list_filter = ("date_joined",)
    empty_value_display = "-пусто-"