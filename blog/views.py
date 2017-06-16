from django.shortcuts import render
from .models import Post
#from .models import SearchISBN, Searchcsv
from .models import Person
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
#from .forms import PostFormisbn
from django.shortcuts import redirect
#from .SearchCSV import searchISBN
from .tables import PersonTable
from django_tables2 import RequestConfig
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
def submit(request):
    myList = request.POST.get('myList',False)
    myList1 = request.POST.get('dropdown-menu',False)
    return render(request, 'blog/test.html',{'myList':myList})

def predict(request):
    myList = request.POST.get('myList',False)
    myList1 = request.POST.get('dropdown-menu',False)
    return render(request, 'blog/predict.html')

def Pricing(request):
    #Command(myList)
    return render(request, 'blog/Pricing.html')

'''def SalesData(request):
    table = PostFormisbn(Searchcsv.objects.all())
    return render(request, 'blog/ISBN.html',{'table': table})'''
    
def person_list(request):
    #table = PersonTable(Person.objects.all())
    table = PersonTable(Person.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'blog/person_list.html', {'table': table})
