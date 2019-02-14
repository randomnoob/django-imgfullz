from django.shortcuts import render
from django.utils import timezone
from .models import Post


def imageface_index(request):
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'imageface_index.html', {'posts': posts})
