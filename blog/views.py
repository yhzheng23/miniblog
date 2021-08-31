from blog.models import Blogger
from django.shortcuts import redirect, render
from .models import Blog,Blogger,Comment
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from .forms import BloggerSignUpForm

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

class BlogDelete(LoginRequiredMixin,DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs')

def BloggerSignup(request):
    if request.method == 'POST':
        form = BloggerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            Blogger.objects.update_or_create(user=user, first_name=user.first_name, last_name=user.last_name)
            user.save()
            user.blogger.save()
            return redirect('login')
    
    else:
        form = BloggerSignUpForm()
    
    context = {
        'form':form,
    }
    return render(request, 'signup.html', context)

class BloggerUpdate(LoginRequiredMixin, UpdateView):
    model = Blogger
    fields = ['first_name', 'last_name', 'self_introduction']

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['time_of_creation', 'content']

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
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

class BlogListbyAuthorView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'
    
    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(Blogger, pk = id)
        return Blog.objects.filter(author=target_author.user)
        
    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(Blogger, pk = self.kwargs['pk'])
        return context

