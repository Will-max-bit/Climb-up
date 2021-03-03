from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    



class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name='users', null=True)

    def __str__(self):
        return self.username
    


class Post(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    post_image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_posts')
    attendees = models.ManyToManyField(User, related_name='attending_posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    scheduled_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
    

