from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chats'
    )

    user_message = models.TextField()
    bot_response = models.TextField()
    intent = models.CharField(
        max_length=50,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_message[:30]}"
    