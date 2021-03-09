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
    posts = Post.objects.all().order_by('-created_date')
    post_data = []
    for post in posts:
        post_data.append({
            'title': post.title,
            'text': post.text,
            'id': post.id,
            'liked_by': request.user in post.likes.all(),
            'attendants': [attendee.username for attendee in post.attendees.all()],
            'likes': post.likes.count(),
            'post_image': post.post_image.url,
            'city': post.city.name,
            'author': post.author.username,
            'created_date': post.created_date.strftime('%b %d %Y'),
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


def post_new(request):
    city_id = request.POST['city_id']
    created_date = request.POST['created_date'],
    scheduled_date = request.POST['scheduled_date'],
    post = Post(
        title = request.POST['title'],
        text = request.POST['text'],
        post_image = request.FILES['post_image'],
        city = City.objects.get(id=city_id),
        author = request.user,
        scheduled_date = request.POST['scheduled_date'],
    )
    post.save()
    return HttpResponse('Ok Morty')

    
def get_cities(request):
    cities = City.objects.all()
    city_data = []
    for city in cities:
        city_data.append({
            'name':city.name,
            'id': city.id,
        })
    return JsonResponse({'cities': city_data})

def add_city(request):
    city_name = request.POST['city_add']
    city = City(
        name = city_name
    )
    city.save()
    return HttpResponse('city added')

@login_required()
def like_post(request):
    post_id = request.GET['post_id']
    post = Post.objects.get(id=post_id)
    user = request.user
    liked_by = True
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked_by = False
    else:
        post.likes.add(user)
        liked_by = True
    likes = post.likes.count()
    response = { 'likes': likes, 'liked_by': liked_by}
    
    #respond with json containing the current number of likes and a boolean indicating whether the current user likes it
    return JsonResponse(response)
    
@login_required()
def attendants(request):
    # return HttpResponse('meet up')
    post_id = request.GET['post_id']
    post = Post.objects.get(id=post_id)
    user = request.user
    # attended_by = user.username
    if post.attendees.filter(id=user.id).exists():
        post.attendees.remove(user)
        attended_by = ''
    else:
        post.attendees.add(user)
        attended_by = user.username
    attendees = post.attendees.all()
    attendee_data = []
    for user in attendees:
        attendee_data.append(user.username)
    print(attendee_data)
    response = {'attendees': attendee_data, 'attended_by': attended_by}
    return JsonResponse(response)
    
@login_required
def post_edit(request):
    city_id = request.POST['city_id']
    created_date = request.POST['created_date'],
    scheduled_date = request.POST['scheduled_date'],
    post = Post(
        title = request.POST['title'],
        text = request.POST['text'],
        post_image = request.FILES['post_image'],
        city = City.objects.get(id=city_id),
        author = request.user,
        scheduled_date = request.POST['scheduled_date'],
    )
    post.save()
    
