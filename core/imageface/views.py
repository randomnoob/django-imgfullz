from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Post


# def imageface_index(request):
#     posts = Post.objects.all().order_by('published_date')
#     return render(request, 'imageface_index.html', {'posts': posts})

class HomeView(ListView):
    model = Post
    template_name = 'album.html'

class SingleView(DetailView):
    model = Post
    template_name = 'single.html'