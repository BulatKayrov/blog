from django.core.cache import cache
from django.shortcuts import render, redirect, reverse

from .forms import CommentForm, PostForm
from .models import Post, Comment
from .utils import slugify, get_post_in_cache


def remove_post(request, slug):
    Post.objects.get(slug=slug).delete()
    return redirect(request.META['HTTP_REFERER'])


def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            created_post = form.save(commit=False)
            created_post.author = request.user
            created_post.slug = slugify(created_post.title)
            created_post.save()
            return redirect(reverse('blog:index'))

    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'blog/create_post.html', context=context)


def index(request, slug_tag=None, slug_category=None):
    posts = get_post_in_cache()

    if slug_tag:
        posts = posts.filter(tags__slug=slug_tag)

    elif slug_category:
        posts = posts.filter(category__slug=slug_category)

    context = {
        'posts': posts
    }
    return render(request=request, template_name='blog/index.html', context=context)


def post_detail(request, slug_post=None):
    if request.method == "POST":
        form = CommentForm(data=request.POST)

        if form.is_valid():

            if request.user.is_authenticated:
                Comment.objects.create(
                    post=Post.objects.get(slug=slug_post),
                    author=request.user,
                    text=form.cleaned_data['text'],
                )
                return redirect(request.META['HTTP_REFERER'])

            else:
                return redirect(reverse('users:login'))
    else:
        form = CommentForm()

    get_post = cache.get('post')
    if get_post:
        post = get_post
    else:
        post = (Post.objects.all().
                select_related('author', 'category',).
                prefetch_related('tags',).
                get(slug=slug_post))
        cache.set('post', post, 60)

    context = {
        'post': post,
        'form': form,
    }
    return render(request=request, template_name='blog/post_detail.html', context=context)
