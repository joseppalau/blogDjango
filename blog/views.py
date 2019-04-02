from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import PostForm, CommentForm, UserForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_frontend = {'posts': posts}
    return render(request, 'blog/post_list.html', stuff_frontend)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.visits += 1
    post.save()
    stuff_frontend = {'post': post}
    return render(request, 'blog/post_detail.html', stuff_frontend)


# Create your views here.

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        title = "New Post"
        stuff_frontend = {'form': form, 'title': title}
    return render(request, 'blog/post_edit.html', stuff_frontend)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pk = pk
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        title = "Edit Post"
        stuff_frontend = {'form': form, 'title': title, 'post': post}
    return render(request, 'blog/post_edit.html', stuff_frontend)


@login_required
def draft_post(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_frontend = {'posts': posts}
    return render(request, 'blog/post_draft_list.html', stuff_frontend)


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
        stuff_frontend = {'form': form}
        return render(request, 'blog/add_comment_to_post.html', stuff_frontend)

@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=pk)

@login_required
def remove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'blog/signup.html', {'form': form})
