from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, Http404, HttpResponse
from django.http import HttpResponse
from .models import Post, City, User
from django.http import HttpResponse, JsonResponse
import json
# Create your views here.


def index(request):
    return render(request, 'climbupApp/index.html')

def load_posts(request):
    # getting posts out of database
    posts = Post.objects.all()
    post_data = []
    for post in posts:
        post_data.append({
            'title': post.title,
            'text': post.text,
            'post_image': post.post_image.url,
            'city': post.city.name,
            'author': post.author.username,
            'created_date': post.created_date
        })
    return JsonResponse({'posts': post_data,})

def profile_page(request):
    return render(request, 'climbupApp/profile_page.html' )


def profile_load(request):
    profile_posts = Post.objects.filter(author=request.user).order_by('-created_date')
    profile_data = []
    for post in profile_posts:
        profile_data.append({
            'title': post.title,
            'text': post.text,
            'post_image': post.post_image.url,
            'city': post.city.name,
            'author': post.author.username,
            'created_date': post.created_date
        })
    return JsonResponse({'profile_posts': profile_data})