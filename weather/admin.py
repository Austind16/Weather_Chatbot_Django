from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "user_message",
        "intent",
        "city",
        "created_at",
    )

    list_filter = (
        "intent",
        "city",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user_message",
        "bot_response",
        "city",
    )

    ordering = (
        "-created_at",
    )