from django.forms import ModelForm, forms
from django import forms

from .models import *


# Создаём модельную форму
class NewsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'выберите автора'

    class Meta:
        model = Post
        fields = ['title','content', 'text', 'author', 'category']
        widgets = {'text': forms.Textarea(attrs={'cols': 60, 'rows': 10})}