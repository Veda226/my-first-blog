from django import forms

from .models import Post
#from .edatotal import test

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
