from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


LIMITATION = 10
POST_DETAIL_LETTERS = 30


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, LIMITATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {'page_obj': page_obj,
               'title': title
               }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts_of_group.all().order_by('-pub_date')
    paginator = Paginator(posts, LIMITATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/group_list.html'
    title = f'Записи сообщества "{group}"'
    context = {'group': group,
               'page_obj': page_obj,
               'title': title,
               }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = User.objects.get(username=username)
    name = user.username
    post_list = Post.objects.filter(author=user.id).order_by('-pub_date')
    paginator = Paginator(post_list, LIMITATION)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profile_title = f'Профайл пользователя {name}'
    count = Post.objects.filter(author=user.id).count()
    context = {'name': name,
               'count': count,
               'page_obj': page_obj,
               'profile_title': profile_title,
               }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_object = Post.objects.get(pk=post_id)
    post_title = post_object.text[:POST_DETAIL_LETTERS]
    post_text = post_object.text
    date = post_object.pub_date
    name_of_author = post_object.author
    author_object = Post.objects.filter(author=name_of_author).count()
    post_group = post_object.group
    post_id = post_id
    context = {'post_title': post_title,
               'name_of_author': name_of_author,
               'author_object': author_object,
               'date': date,
               'post_group': post_group,
               'post_text': post_text,
               'post_object': post_object,
               'post_id': post_id,
               }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.pk
            post.save()
            return redirect('posts:profile', username=request.user)
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True

    if request.method == 'POST' and request.user.pk == post.author_id:
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.pk
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        if request.user.pk != post.author_id:
            return render(request, 'posts:post_detail', {'form': form})

    context = {'form': form,
               'post': post,
               'is_edit': is_edit,
               }
    return render(request, 'posts/create_post.html', context)
