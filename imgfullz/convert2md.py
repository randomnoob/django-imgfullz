# -*- coding: utf-8 -*- #

import os
import jsonlines
from jsonlines.jsonlines import InvalidLineError
from slugify import slugify as slugify_url
import time
from progressbar import ProgressBar



DATA_INPUT_PATH = '/media/nl/linix5001/new/600k-1/'
if DATA_INPUT_PATH[-1] == '/':
    DATA_INPUT_PATH = DATA_INPUT_PATH[:-1]
input_parse = os.path.split(DATA_INPUT_PATH)
DATA_OUTPUT_PATH = os.path.join(input_parse[0], '{}_converted'.format(input_parse[1]))
print (DATA_OUTPUT_PATH)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


class Post:
    def __init__(self, title):
        """
        title, slug, content are things that defines a post
        content should be a dict grabbed from Google
        """
        self.title = title
        self.slug = slugify_url(title)
        self.meta = ''
        self.content = ''
        self.content_skeleton = '![{image_alt}]({image_url} "{image_alt}  ©Image courtesy of {image_refername} {image_referurl}")\n\n'
        self.footer = ''
        self.num_images = 0


    def insert_contentblock(self, image_meta_dict):
        if self.num_images < 50:
            skeleton_dict = {}
            skeleton_dict['image_url'] = image_meta_dict.get('ou')
            skeleton_dict['image_alt'] = image_meta_dict.get('s')
            skeleton_dict['image_referhomepage'] = image_meta_dict.get('rh')
            skeleton_dict['image_referurl'] = image_meta_dict.get('ru')
            skeleton_dict['image_refername'] = image_meta_dict.get('st')

            block = self.content_skeleton.format(**skeleton_dict)
            # print ('---{}---'.format(block))
            if not self.meta:
                self.meta = 'Title: {}\nDate: 2018-12-22\nAuthor: MedDB\nTags: General\nSummary: {}\nSlug: {}\nFeaturedImage: {}\n\n'\
                            .format(self.title, skeleton_dict['image_alt'], self.slug, skeleton_dict['image_url'])
            self.content += block
            self.num_images += 1
            self.footer += " {}".format(skeleton_dict['image_alt'])

    def save(self, filename, path):
        if ".md" not in filename:
            filename = filename + ".md"
        fullpath = os.path.join(path, filename)
        with open(fullpath, 'w', encoding='utf-8') as output:
            output.write(self.meta + self.content + self.footer.strip())
        # print ('Saved {} contains {} blocks'.format(filename, self.num_images), end='\r')



class CoreProcess:
    def __init__(self, output_path=DATA_OUTPUT_PATH, input_path=DATA_INPUT_PATH):
        """
        :param output_path: Destination directory that stores the output content
        :param input_path: Source directory that stores the input content
        """
        self.output_path = output_path
        self.input_path = input_path

        # If output_path doesn't exist -> make one
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
    # -------------------------------
    # Directory manipulation
    @staticmethod
    def all_dirs(path):
        paths = []
        for dir in os.listdir(path):
            if os.path.isdir(path + '/' + dir):
                paths.append(path + '/' + dir)

        return paths
    @staticmethod
    def all_files(path):
        paths = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.isfile(path + '/' + file):
                    paths.append(path + '/' + file)
        return paths
    @staticmethod
    def get_files_tuple(path):
        downloaded = []
        for root, dirs, files in os.walk(path):
            for file in files:
                fullpath = path + '/' + file
                if os.path.isfile(fullpath):
                    tup = (fullpath,os.path.splitext(file)[0]) #first the path, then the filename
                    downloaded.append(tup)
        return downloaded
    @staticmethod
    def make_dir(dirname):
        current_path = os.getcwd()
        path = os.path.join(current_path, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
    # -------------------------------
    def get_queues(self):
        return self.get_files_tuple(self.input_path)

    def transform_post(self, input_file_tup):
        try:
            post = Post(input_file_tup[1])
            with jsonlines.open(input_file_tup[0], mode='r') as reader:
                for dic in reader:
                    post.insert_contentblock(dic)
                post.save(post.slug, self.output_path)
        except InvalidLineError:
            pass


    @timeit
    def do_transform(self):
        queues = self.get_queues()
        _progress = ProgressBar()
        for file_tup in _progress(queues):
            self.transform_post(file_tup)



core = CoreProcess()
core.do_transform()




