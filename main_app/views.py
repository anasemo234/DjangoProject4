from distutils import extension
from multiprocessing import context
from re import template
from wsgiref import validate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Blog, Photo
from .forms import FoodForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

# Create your views here.

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'explor-avatar-31'


def home(request):
    
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def allblogs(request):
    allblog = Blog.objects.all()
    return render(request, 'all.html')


def blogs_index(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, 'blogs/index.html', {'blogs': blogs})


@login_required
def blogs_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    # FoodForm to be rendered in the template
    food_form = FoodForm()
    return render(request, 'blogs/detail.html', {
        # including the cat and food_form in the context
        'blog': blog, 'food_form': food_form})


@login_required
def add_food(request, blog_id):
    # create the ModelForm using the data in request.POST
    form = FoodForm(request.POST)
    # validate the form
    if form.is_valid():
        # dont save the form to the db until it has blog_id assigned
        new_food = form.save(commit=False)
        new_food.blog_id = blog_id
        new_food.save()
    return redirect('detail', blog_id=blog_id)


@login_required
def add_photo(request, blog_id):
    # photo_file will be the 'name' attribute on the <input type='file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # needs a unique 'key' for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
                         photo_file.name[photo_file.name.rfind('.'):]
        # in case something is wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # assign to blog_id or blog (if you have a blog obj)
            photo = Photo(url=url, blog_id=blog_id)
            photo.save()
        except Exception as error:
            print('Error uploading  photo: ', error)
            return redirect('detail', blog_id=blog_id)
    return redirect('detail', blog_id=blog_id)


class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('name', 'location', 'description')
    success_url = '/blogs/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['location', 'description']


class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = '/blogs/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again!'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
