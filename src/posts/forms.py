from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class SearchForm(forms.Form):
    query  = forms.CharField(max_length = 100, required = False, label = 'Search')