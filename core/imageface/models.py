from django.db import models
from django.utils import timezone
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)


class Images(models.Model):
    link = models.CharField(max_length=400)
    description = models.CharField(max_length=250, null=True)
    source_page = models.CharField(max_length=400)
    source_page_title = models.CharField(max_length=300, null=True)
    source_site_title = models.CharField(max_length=250, null=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images')
