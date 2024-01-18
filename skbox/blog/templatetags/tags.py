from django import template
from django.core.cache import cache

from blog.models import Tag

register = template.Library()


@register.simple_tag
def tag_list():
    tags = cache.get('tags')
    if tags is None:
        get_tags = Tag.objects.all()
        cache.set('tags', get_tags, 50)
        return get_tags
    return tags
