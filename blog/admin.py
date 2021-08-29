from django.contrib import admin
from .models import Blog,Blogger, Comment

# Register your models here.
admin.site.register(Blogger)

class CommentInline(admin.TabularInline):
    model = Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author')
    inlines = [CommentInline]

admin.site.register(Blog,BlogAdmin)