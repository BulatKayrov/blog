from django.urls import path

from .views import index, post_detail, create_post, remove_post

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('tags/<slug:slug_tag>/', index, name='tag'),
    path('categories/<slug:slug_category>/', index, name='category'),
    path('post/<slug:slug_post>/', post_detail, name='detail'),
    path('create/', create_post, name='create_post'),
    path('delete/<slug:slug>', remove_post, name='remove_post'),
]
