from django import forms
from .models import Post,Searchcsv

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class PostFormisbn(forms.ModelForm):
    class Meta:
        model = Searchcsv
        fields = ('Year','P',)
