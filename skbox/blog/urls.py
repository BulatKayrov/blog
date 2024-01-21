from django.urls import path

from .views import (
    PostListView,
    # post_detail,
    # create_post,
    remove_post,
    PostDetailView, PostCreateView
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('tags/<slug:slug_tag>/', PostListView.as_view(), name='tag'),
    path('categories/<slug:slug_category>/', PostListView.as_view(), name='category'),
    # path('post/<slug:slug_post>/', post_detail, name='detail'),
    path('post/<slug:slug_post>/', PostDetailView.as_view(), name='detail'),
    # path('create/', create_post, name='create_post'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('delete/<slug:slug>', remove_post, name='remove_post'),
]
