from blog.models import Blogger
from django.shortcuts import render
from .models import Blog,Blogger,Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse

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

class BloggerListView(generic.ListView):
    model = Blogger
    paginate_by = 5

class BloggerDetailView(generic.DetailView):
    model = Blogger

class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'time_of_creation', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdate(LoginRequiredMixin,UpdateView):
    model = Blog
    fields = ['title', 'content']

class BloggerUpdate(LoginRequiredMixin, CreateView):
    model = Blogger
    fields = ['first_name', 'last_name', 'self_introduction']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['time_of_creation', 'content']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.commenter = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super().form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})


