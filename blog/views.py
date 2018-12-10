from django.shortcuts import render
from .models import Post
from django.utils import timezone


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    stuff_front_end = {'posts': posts}
    return render(request, 'blog/post_list.html', stuff_front_end)

# Create your views here.
