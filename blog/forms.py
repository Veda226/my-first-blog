from django import forms
from .models import Post
import django_tables2 as tables
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

'''class PostFormisbn(tables.Table):
    class Meta:
        model = SearchISBN
#        fields = ('Year','P',)'''
