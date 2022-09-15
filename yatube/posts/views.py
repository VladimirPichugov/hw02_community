from django.shortcuts import render, get_object_or_404
from .models import Post, Group


LIMITATION = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:LIMITATION]
    title = 'Последние обновления на сайте'
    context = {'posts': posts,
               'title': title
               }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts_of_group.all().order_by('-pub_date')[:LIMITATION]
    template = 'posts/group_list.html'
    title = f'Записи сообщества "{group}"'
    context = {'group': group,
               'posts': posts,
               'title': title
               }
    return render(request, template, context)
