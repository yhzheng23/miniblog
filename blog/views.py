from blog.models import Blogger
from django.shortcuts import render
from .models import Blog,Blogger,Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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
        'num_visits':num_visits,
    }

    return render(request,'index.html',context=context)


class BlogListView(generic.ListView):
    model = Blog
    paginate_by = 5

class BlogDetailView(generic.DetailView):
    model = Blog

class BloggerDetailView(generic.DetailView):
    model = Blogger

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'time_of_creation', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BloggerUpdate(LoginRequiredMixin, CreateView):
    model = Blogger
    fields = ['first_name', 'last_name', 'self_introduction']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

