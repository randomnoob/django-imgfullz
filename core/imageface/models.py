from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.postgres.fields import JSONField
import json
import random


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True)
    text = models.TextField()
    contents = JSONField(null=True)
    published_date = models.DateTimeField(default=timezone.now)

    @property
    def thumbnail(self):
        "Returns the first image found in obj.contents"
        data = json.loads(self.contents)
        return data.get('metadata')[0]['ou']

    @property
    def images(self):
        "Returns a list of all image urls from obj.contents"
        data = json.loads(self.contents)
        return [x['ou'] for x in data['metadata'] if x.get('ou')]

    @property
    def views(self):
        "Returns a random view count"
        return random.randint(300,3000)
