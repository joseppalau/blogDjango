from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_frontend = {'posts': posts}
    return render(request, 'blog/post_list.html', stuff_frontend)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    stuff_frontend = {'post': post}
    return render(request, 'blog/post_detail.html', stuff_frontend)
# Create your views here.


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
        stuff_frontend = {'form': form, 'title': title}
    return render(request, 'blog/post_edit.html', stuff_frontend)


def draft_post(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    stuff_frontend = {'posts':posts}
    return render(request, 'blog/post_draft_list.html', stuff_frontend)


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect(request, 'blog/post_list.html')


