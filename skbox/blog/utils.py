from django.template.defaultfilters import slugify as django_slugify
from django.core.cache import cache

from blog.models import Post

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def get_post_in_cache():
    posts = cache.get('posts')

    if posts is None:
        posts = Post.objects.all()
        cache.set('posts', posts, 30)
        return posts
    return posts


def get_in_cache_name_post(slug_post):
    name = f'post_{slug_post}'
    get_post = cache.get(name)
    if get_post:
        return get_post
    post = (Post.objects.all().
            select_related('author', 'category', ).
            prefetch_related('tags', ).
            get(slug=slug_post))
    cache.set(name, post, 60)
    return post
