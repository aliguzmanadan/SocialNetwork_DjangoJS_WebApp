from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, ManyToManyField

import network


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

    def set_following(self):
        """Returns a set with all Users followed by this user"""
        return set([rel.followed for rel in self.followed.all()])

    def set_followers(self):
        """Returns a se wtith all followers of this user"""
        return set([rel.follower for rel in self.followers.all()])

    def NumberFollowers(self):
        return len(self.set_followers())

    def NumberFollowing(self):
        return len(self.set_following())

    def is_follower(self, another_user):
        """Returns a boolean value depending on whether self follows another_user"""
        return self in another_user.set_followers()

#Create a separate class "Following" to instance each following relation.
class Following(models.Model):
    followed = ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = ForeignKey(User, on_delete=models.CASCADE, related_name="followed")

    def __str__(self):
        return f"Follower: {self.follower}, Followed: {self.followed}"


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