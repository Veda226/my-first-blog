from django.contrib import admin

# Register your models here.
from .models import Post
from .models import SearchISBN
admin.site.register(Post)

