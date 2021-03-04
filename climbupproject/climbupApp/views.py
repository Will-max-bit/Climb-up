from django.shortcuts import render, HttpResponseRedirect, reverse, redirect, Http404, HttpResponse
from django.http import HttpResponse
from .models import Post, City
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

## renders the homepage with all posts
def index(request):
    return render(request, 'climbupApp/index.html')

# provides the data to be rendered on the home page
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

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('climbupApp:index')
        else:
            messages.info(request, 'invalid username or password')
    # return render(request, 'climbupApp/login.html', {})
    return render(request, 'climbupApp/login_page.html')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            profile_image = form.cleaned_data['image']
            user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password1'])
            # user_profile = User(user = user, profile_image = profile_image)
            # user_profile.save()

            messages.success(request, f'Account created for{user.username}')
            login(request, user)
            return redirect('climbupApp:index')
        else:
            return render(request, 'climbupApp/register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'climbupApp/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('climbupApp:index')

@login_required
def post_new(request):
    post_data = json.loads(request.body)
    title = post_data['title']
    text = post_data['text']
    post_image = post_data['post_image']
    city = post_data['city']
    author = post_data['author']
    attendees = post_data['attendees']
    likes = post_data['likes']
    created_date = post_data['created_date']
    schedules_date = post_data['scheduled_date']
    post = Post(title=title, text=text, post_image=post_image, city=city, author=author, attendees=attendees, likes=likes, created_date=created_date, scheduled_date=scheduled_date)
    post.save()

    return HttpResponse('Ok Morty')








# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             django.contrib.auth.login(request, user)
#             messages.success(request, 'login successful')
#         else:
#             messages.info(request, 'invalid username or password')
#     return render(request, 'climbupApp/login.html', {})
