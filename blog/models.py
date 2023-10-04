from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    country = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.username
    

class Blog(models.Model):
    title = models.CharField(max_length=225,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


 

