from django import template
from abisionapp.models import Post 
from django.db.models import Count
register = template.Library()

@register.simple_tag
#@register.simple_tag(name='my_tags')
def total_posts():
    return Post.objects.count()

@register.inclusion_tag('BlogApp/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]