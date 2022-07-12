from distutils import extension
from re import template
from wsgiref import validate
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Blog, Photo
from .forms import FoodForm
import uuid
import boto3

# Create your views here.

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'explor-avatar-31'


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



def add_photo(request, blog_id):
    # photo_file will be the 'name' attribute on the <input type='file'>
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # needs a unique 'key' for S3 / needs image file extension too
        key = uuid.uuid4(),hex[:6] + photo_file.name[photo_file.name.rfind['.']:]
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