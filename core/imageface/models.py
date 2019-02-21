from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
import json
import random


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True)
    contents = JSONField(null=True)
    published_date = models.DateTimeField(default=timezone.now)

    @property
    def thumbnail(self):
        "Returns the first image found in obj.contents"
        data = json.loads(self.contents)
        return data.get('metadata')[0]['ou']

    @property
    def thumbnail_description(self):
        "Returns the first image found in obj.contents"
        data = json.loads(self.contents)
        return data.get('metadata')[0]['s']

    @property
    def images(self):
        "Returns a list of all image urls from obj.contents"
        data = json.loads(self.contents)
        return [{'url': x['ou'], 'alt': x['s']} for x in data['metadata'] if x.get('ou')]

    @property
    def imagedata(self):
        "Returns a list of dict of all image data from obj.contents"
        data = json.loads(self.contents)
        return data['metadata']

    def get_absolute_url(self):
        return reverse('single_post_slug',kwargs={'slug':self.slug, 'pk': self.pk})