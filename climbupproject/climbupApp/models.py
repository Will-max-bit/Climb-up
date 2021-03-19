from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
        return self.title + 'by' + self.author.username + 'on' + self.created_date.strftime('%b %d %Y')
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # name = models.CharField(max_length=80)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_authors')
    # email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']
    
    def __str__(self):
        return 'Comment {} by {}'. format(self.body, self.author)
    