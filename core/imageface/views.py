from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post



class HomeView(ListView):
    # model = Post
    template_name = 'index.html'
    paginate_by = 20
    def get_queryset(self):
        all_posts = Post.objects.all().count()
        last200 = Post.objects.filter(pk__gte=all_posts-200)
        return last200

class SinglePostIDView(DetailView):
    model = Post
    template_name = 'single.html'

class SinglePostSlugView(DetailView):
    model = Post
    template_name = 'single.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images_page = self.request.GET.get("page")
        # post_images = self.object.images
        # post_images_paginator = Paginator(post_images, self.paginate_by)
        # # Catch invalid page numbers
        # try:
        #     paginated_images_obj = post_images_paginator.page(images_page)
        # except (PageNotAnInteger, EmptyPage):
        #     paginated_images_obj = post_images_paginator.page(1)
        # context['paginated_images'] = paginated_images_obj

        post_images_data = self.object.imagedata
        post_images_data_paginator = Paginator(post_images_data, self.paginate_by)
        # Catch invalid page numbers
        try:
            post_images_data_paginator_obj = post_images_data_paginator.page(images_page)
        except (PageNotAnInteger, EmptyPage):
            post_images_data_paginator_obj = post_images_data_paginator.page(1)
        context['paginated_images'] = post_images_data_paginator_obj
        context['paginated_text'] = " ".join([x['s'] for x in post_images_data_paginator_obj.object_list])

        posts = Post.objects.filter(pk__lte=500,pk__gte=100)
        context['last_posts'] = posts[60:66]
        context['most_viewed_posts'] = posts[20:24]
        context['featured_posts'] = posts[16:20]

        return context


class ArchiveView(ListView):
    model = Post
    template_name = 'archive.html'
    paginate_by = 20
