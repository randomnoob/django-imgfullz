import os
import json
import time
import traceback
from imageface.models import Post
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import DataError, IntegrityError
from django.utils.text import slugify
from json.decoder import JSONDecodeError


DATA_INPUT_PATH = '/media/nl/New Volume/vietnamese-74k'


def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)


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


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    @staticmethod
    def get_files(directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))

    def parse_json_new_format(self, json_path):
        try:
            print ("Opening {}".format(json_path))
            with open(json_path, 'r') as input:
                reader = json.load(input)
                keyword = reader['keyword']
                slug = slugify(keyword, allow_unicode=True)
                _user, user_is_created = get_user_model().objects.get_or_create(pk=1)
                _post, post_is_created = Post.objects.get_or_create(
                    author=_user, title=keyword, slug=slug, contents=json.dumps(reader))
                print('-----\n{} ==> {}\n-----'.format(keyword, slug))
        except (DataError, IntegrityError, JSONDecodeError):
            traceback.print_exc()
            pass

    def parse_all_directory(self, path):
        all_files = self.get_files(path)
        for index, file in enumerate(all_files):
            print("Processing entry number {}".format(index+1))
            self.parse_json_new_format(file)

    @timeit
    def handle(self, *args, **options):
        self.parse_all_directory(DATA_INPUT_PATH)
