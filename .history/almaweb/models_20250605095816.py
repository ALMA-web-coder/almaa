from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField




# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=400)
    abstract = models.TextField()
    document = models.FileField(upload_to='documents/')
    author = models.CharField(max_length=100) 
    published_date = models.DateField(auto_now_add=True) 
    def __str__(self):
        return self.title
    

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True) 
    content = HTMLField()
    author = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)  
    abstract = models.TextField()

    def __str__(self):

        return self.title
    

class Comment(models.Model):
    news_item = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)  # Link to the News model
    comment = models.TextField(blank=True, null=True)
    email = models.EmailField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email