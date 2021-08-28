from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Blogger',on_delete=models.SET_NULL,null=True)
    time_of_creation = models.DateTimeField(default=datetime.now, null=True,blank=True)
    tag = models.ManyToManyField('Tag',help_text='add a tag for this blog')
    content = models.TextField(max_length=5000)

    class Meta:
        ordering = ['-time_of_creation']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def display_tag(self):
        return ', '.join(tag.name for tag in self.tag.all()[:3])
    
    display_tag.short_description = 'tag'

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='enter a blog tag'
    )

    def __str__(self):
        return self.name

class Blogger(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    self_introduction = models.TextField(max_length=500)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

class Comment(models.Model):
    blog = models.ForeignKey('Blog', on_delete=models.SET_NULL,null=True)
    commenter = models.ForeignKey('Blogger',on_delete=models.SET_NULL,null=True)
    time_of_creation = models.DateTimeField(default=datetime.now,null=True,blank=True)
    content = models.TextField(max_length=500)

    class Meta:
        ordering = ['-time_of_creation']
    
    def __str__(self):
        return f'{self.commenter}@{self.time_of_creation} - {self.content[:75]}'
    
    def get_absolute_url(self):
        return reverse('comment-detail', args=[str(self.id)])

