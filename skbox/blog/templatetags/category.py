from django import template
from django.core.cache import cache

from blog.models import Category

register = template.Library()


@register.simple_tag
def category_list():
    category = cache.get('category')
    if not category:
        category = Category.objects.all()
        cache.set('category', category, 15)
        return category
    return category
