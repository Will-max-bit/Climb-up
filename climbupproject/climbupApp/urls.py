from django.urls import path
from . import views

app_name='climbupApp'
urlpatterns = [
    path('', views.index, name='index'),
    path('load_posts/', views.load_posts, name='load_posts'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('profile_load/', views.profile_load, name='profile_load'),
    path('login_page/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('logout_user/', views.logout_user, name='logout_user'),
]
