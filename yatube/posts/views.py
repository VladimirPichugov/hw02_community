from django.shortcuts import render, get_object_or_404
from .models import Post, Group


N_O_P = 10 #  NUMBER_OF_POSTS


# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:N_O_P]
    title = 'Последние обновления на сайте'
    context = {'posts': posts,
               'title': title
               }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:N_O_P]
    template = 'posts/group_list.html'
    title = f'Записи сообщества "{group}"'
    context = {'group': group,
               'posts': posts,
               'title': title
               }
    return render(request, template, context)
