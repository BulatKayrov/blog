from django import template

from blog.models import Tag

register = template.Library()


@register.simple_tag
def category_list():
    return Tag.objects.all()
