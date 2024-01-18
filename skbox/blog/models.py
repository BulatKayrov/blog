from django.db import models
from django.shortcuts import reverse, redirect
from django.template.defaultfilters import slugify

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=155, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=155, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug_category': self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=155, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=155, unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        db_table = 'tag'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug_tag': self.slug})


class Post(models.Model):
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', blank=True, null=True)
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    body = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=None, null=True,
        verbose_name='Автор', blank=True, related_name='posts'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    tags = models.ManyToManyField(to='Tag', verbose_name='Теги', related_name='posts')
    category = models.ForeignKey(
        to=Category, on_delete=models.SET_DEFAULT, default=None,
        null=True, verbose_name='Категория', blank=True, related_name='posts'
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        db_table = 'post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug_post': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comment', verbose_name='Комментарий')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='comment', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст', max_length=255)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        db_table = 'comment'

