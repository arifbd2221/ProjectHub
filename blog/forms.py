from django import forms
from .models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'github_link', 'presentation_link', 'sellable', 'price']