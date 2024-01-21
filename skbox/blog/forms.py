from django import forms

from blog.models import Comment, Post
from .utils import slugify, get_post_in_cache


class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('text',)

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.author = self.context.get('author')
        comment.post = self.context.get('post')
        comment.text = self.cleaned_data['text']
        comment.save()
        return comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'body', 'tags', 'category')

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        # post.author = self.request.user
        post.slug = slugify(post.title)
        data = self.cleaned_data['tags']
        post.save()

        for tag in data:
            post.tags.add(tag)

        return post


