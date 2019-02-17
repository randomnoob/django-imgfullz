from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True)
    text = models.TextField()
    contents = JSONField(null=True)
    published_date = models.DateTimeField(default=timezone.now)