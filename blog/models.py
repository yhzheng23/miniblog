from django.db import models
from datetime import datetime
import uuid
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='uuid for this blog')
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Blogger',on_delete=models.SET_NULL,null=True)
    time_of_creation = models.DateTimeField(null=True,blank=True)
    tag = models.ManyToManyField('Tag',help_text='add a tag for this blog')
    content = models.TextField(max_length=5000)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def display_tag(self):
        return ','.join(tag.name for tag in self.tag.all()[:3])

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='enter a blog tag'
    )

    def __str__(self):
        return self.name

class Blogger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    self_introduction = models.TextField(max_length=500)

    class Meta:
        ordering = ['last_name','first_name']

    def __str__(self):
        return f'{self.first_name},{self.last_name}'

    def get_absolute_url(self):
        return reverse('blogger-detail', args=[str(self.id)])

class Comment(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='uuid for this comment')
    blog = models.ForeignKey('Blog', on_delete=models.SET_NULL,null=True)
    commenter = models.ForeignKey('Blogger',on_delete=models.SET_NULL,null=True)
    time_of_creation = models.DateTimeField(null=True,blank=True)
    content = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.commenter}:{self.content}'
    
    def get_absolute_url(self):
        return reverse('comment-detail', args=[str(self.id)])

