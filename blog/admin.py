from django.contrib import admin
from .models import Blog,Blogger, Comment,Tag

# Register your models here.
admin.site.register(Blogger)
admin.site.register(Tag)

class CommentInline(admin.TabularInline):
    model = Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_tag')
    inlines = [CommentInline]

admin.site.register(Blog,BlogAdmin)