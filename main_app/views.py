from django.shortcuts import render
# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')



class Blog:
    def __init__(self, name, location, description,):
        self.name = name
        self.location = location
        self.description = description


blogs = [
    Blog('Anasemos', 'Cancun, Mexico', 'View of Tulum')
]


def blogs_index(request):
    return render(request, 'blogs/index.html', {'blogs': blogs})