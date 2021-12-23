from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField


class User(AbstractUser):
    follows = ManyToManyField("self", blank=True, related_name="followers")

class Post(models.Model):
    poster = ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = ManyToManyField(User, blank=True, related_name="liked_posts")

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": 0
        }