from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post

def get_redirected(queryset_or_class, lookups, validators):
    """
    Calls get_object_or_404 and conditionally builds redirect URL
    """
    obj = get_object_or_404(queryset_or_class, **lookups)
    for key, value in validators.items():
        if value != getattr(obj, key):
            return obj, obj.get_absolute_url()
    return obj, None

def my_view(request, slug, id):
    article, article_url = get_redirected(Post, {'pk': id}, {'slug': slug})
    if article_url:
        return redirect(article_url)


class HomeView(ListView):
    model = Post
    template_name = 'album.html'

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

        posts = Post.objects.filter(published_date__lte=timezone.now())
        context['last_posts'] = posts[:6]
        context['most_viewed_posts'] = posts[16:22]

        return context