from re import template
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Blog
from .forms import FoodForm
# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def blogs_index(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs/index.html', {'blogs': blogs})

def blogs_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # FoodForm to be rendered in the template
    food_form = FoodForm()
    return render(request, 'blogs/detail.html', {
        # including the cat and food_form in the context
        'blog': blog, 'food_form': food_form})


class BlogCreate(CreateView):
    model = Blog
    fields = '__all__'
    success_url = '/blogs/'

class BlogUpdate(UpdateView):
    model = Blog
    fields = ['location', 'description']

class BlogDelete(DeleteView):
    model = Blog
    success_url = '/blogs/'