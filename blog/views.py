from blog.models import Blogger
from django.shortcuts import render
from .models import Blog,Blogger,Comment
from django.views import generic

# Create your views here.
def index(request):
    num_bloggers = Blogger.objects.all().count
    num_blogs = Blog.objects.all().count
    num_comments = Comment.objects.all().count

    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_bloggers': num_bloggers,
        'num_blogs':num_blogs,
        'num_comments':num_comments,
    }

    return render(request,'index.html',context=context)


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

class BlogDetailView(generic.DetailView):
    model = Blog

class BloggerDetailView(generic.DetailView):
    model = Blogger


