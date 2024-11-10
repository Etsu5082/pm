# main_app/models.py

from django.db import models
from django.contrib.auth.models import User

class Practice(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=255, default='Unknown')
    is_closed = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(default=10)  # 定員を示すフィールド

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} at {self.location}"

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'practice'], name='unique_user_practice')
        ]
        indexes = [
            models.Index(fields=['user', 'practice']),
        ]

    def __str__(self):
        return f"{self.user.username} registered for {self.practice}"
