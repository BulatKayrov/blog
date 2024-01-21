from django.core.cache import cache
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from .forms import CommentForm, PostForm
from .models import Post, Comment
from .utils import slugify, get_post_in_cache, get_in_cache_name_post


class PostListView(ListView):
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    def queryset(self):
        return get_post_in_cache()

    def get_queryset(self):
        queryset = self.queryset()

        slug_tag = self.kwargs.get('slug_tag')
        slug_category = self.kwargs.get('slug_category')

        if slug_tag:
            queryset = queryset.filter(tags__slug=slug_tag)

        if slug_category:
            queryset = queryset.filter(category__slug=slug_category)

        return queryset


class PostDetailView(View):

    def get(self, request, slug_post):
        form = CommentForm()
        post = get_in_cache_name_post(slug_post)
        context = {
            'post': post,
            'form': form
        }
        return render(request, template_name='blog/post_detail.html', context=context)

    def post(self, request, slug_post):
        context = {
            'post': get_in_cache_name_post(slug_post),
            'author': request.user,
        }
        form = CommentForm(data=request.POST, context=context)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER'))


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    context_object_name = 'form'
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form = super(PostCreateView, self).form_valid(form)
        form.author = self.request.user
        return form


# def post_detail(request, slug_post=None):
#     if request.method == "POST":
#         form = CommentForm(data=request.POST)
#
#         if form.is_valid():
#
#             if request.user.is_authenticated:
#                 Comment.objects.create(
#                     post=Post.objects.get(slug=slug_post),
#                     author=request.user,
#                     text=form.cleaned_data['text'],
#                 )
#                 return redirect(request.META['HTTP_REFERER'])
#
#             else:
#                 return redirect(reverse('users:login'))
#     else:
#         form = CommentForm()
#
#     get_post = cache.get('post')
#     if get_post:
#         post = get_post
#     else:
#         post = (Post.objects.all().
#                 select_related('author', 'category', ).
#                 prefetch_related('tags', ).
#                 get(slug=slug_post))
#         cache.set('post', post, 60)
#
#     context = {
#         'post': post,
#         'form': form,
#     }
#     return render(request=request, template_name='blog/post_detail.html', context=context)


def remove_post(request, slug):
    Post.objects.get(slug=slug).delete()
    return redirect(request.META['HTTP_REFERER'])


# def create_post(request):
#     if request.method == 'POST':
#         print(request.POST)
#         form = PostForm(data=request.POST, files=request.FILES)
#
#         if form.is_valid():
#             form.request = request
#             form.save()
#             return redirect(reverse('blog:index'))
#
#     else:
#         form = PostForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'blog/create_post.html', context=context)

# def index(request, slug_tag=None, slug_category=None):
#     posts = get_post_in_cache()
#
#     if slug_tag:
#         posts = posts.filter(tags__slug=slug_tag)
#
#     elif slug_category:
#         posts = posts.filter(category__slug=slug_category)
#
#     context = {
#         'posts': posts
#     }
#     return render(request=request, template_name='blog/index.html', context=context)
