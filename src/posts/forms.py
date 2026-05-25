from django import forms
from .models import Comment
from .models import Post
from django.forms import ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SearchForm(forms.Form):
    query  = forms.CharField(max_length = 100, required = False, label = 'Search')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body','image', 'tags', 'category']