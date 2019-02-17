import os
import json
import time
from progressbar import ProgressBar
from imageface.models import Post, Images
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


DATA_INPUT_PATH = '/home/nl/dev/django/imgfullz/downloaded-json/'


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


# parse_json('/home/nl/dev/django/imgfullz/downloaded-json/alum.json')

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def get_files(directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))

    def parse_json(self, json_path):
        with open(json_path, 'r') as input:
            reader = json.load(input)
            keyword = reader['keyword']
            metadata = []
            texts = [x['s'] for x in reader['metadata']]
            joined_texts = ' '.join(texts)
            _user, user_is_created = get_user_model().objects.get_or_create(pk=1)
            _post, post_is_created = Post.objects.get_or_create(
                author=_user, title=keyword, text=joined_texts)
            for item in reader['metadata']:
                print('{}\n\n'.format(item))
                obj, created = Images.objects.get_or_create(post=_post, link=item['ou'], description=item['s'],
                                                            source_page=item.get('ru'), source_page_title=item.get('pt'),
                                                            source_site_title=item.get('st'))
                metadata.append((obj))

    def parse_json2(self, json_path):
        """
        Uses JSONField model
        """
        with open(json_path, 'r') as input:
            reader = json.load(input)
            keyword = reader['keyword']
            metadata = []
            texts = [x['s'] for x in reader['metadata']]
            joined_texts = ' '.join(texts)
            _user, user_is_created = get_user_model().objects.get_or_create(pk=1)
            _post, post_is_created = Post.objects.get_or_create(
                author=_user, title=keyword, text=joined_texts, contents=str(metadata))

    def parse_all_directory(self, path):
        all_files = self.get_files(path)
        for index, file in enumerate(all_files):
            print ("Running import number : ", index+1)
            self.parse_json2(file)

    def handle(self, *args, **options):
        self.parse_all_directory(DATA_INPUT_PATH)
