from django.db import models
from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('content',)

        labels = {
            'content': ''
        }

        widgets = {
            'content': forms.Textarea(attrs={'class': "form-control", "rows": 2, 'placeholder': ""})
        }