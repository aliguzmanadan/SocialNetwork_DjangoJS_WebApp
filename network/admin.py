from django.contrib import admin
from .models import User, Post, Following

# Register your models here.
class User_Admin(admin.ModelAdmin):
    list_display = ("username", "email")

class Post_Admin(admin.ModelAdmin):
    list_display = ("poster", "content", "timestamp")

admin.site.register(User, User_Admin)
admin.site.register(Post, Post_Admin)
admin.site.register(Following)