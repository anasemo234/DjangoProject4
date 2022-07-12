from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blogs/', views.blogs_index, name='index'),
    path('blogs/<int:blog_id>/', views.blogs_detail, name='detail'),
    path('blogs/create/', views.BlogCreate.as_view(), name='blogs_create'),
    path('blogs/<int:pk>/update/', views.BlogUpdate.as_view(), name='blogs_update'),
    path('blogs/<int:pk>/delete/', views.BlogDelete.as_view(), name='blogs_delete'),
]