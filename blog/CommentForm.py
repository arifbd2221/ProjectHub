from django import forms
from .models import Comments

class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ('text',)