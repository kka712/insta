from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Post.objects.all()
    form = CommentForm()
    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()

        context = {
            'form': form,
        }

        return render(request, 'create.html', context)


@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
        return redirect('posts:index')


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # if post in user.like_posts.all():
    if user in post.like_users.all():
        # user.like_posts.remove(post)
        post.like_users.remove(user)
    else:
        # user.like_posts.add(post)
        post.like_users.add(user)

    return redirect('posts:index')

def feed(request):
    followings = request.user.followings.all()

    posts = Post.objects.filter(user__in=followings) # 내가 팔로우 하는 사람들이 작성한 게시물들
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'index.html', context)


from django.http import JsonResponse
def like_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'post_id': id,
        'status': status,
        'count': len(post.like_users.all())
    }
    return JsonResponse(context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(title__contains=query)

    context = {
        'posts': posts
    }

    return render(request, 'search.html', context)
