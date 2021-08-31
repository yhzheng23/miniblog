from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/',views.BlogListView.as_view(),name='blogs'),
    path('bloggers/',views.BloggerListView.as_view(),name='bloggers'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(),name='blog-detail'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(),name='blogger-detail'),

    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blog/<int:pk>/update', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', views.BlogDelete.as_view(), name='blog-delete'),
    path('blog/<int:pk>/comment/', views.CommentCreate.as_view(), name='blog-comment'),
    
    path('blogger/signup/', views.BloggerSignup, name='blogger-signup'),
    path('blogger/<int:pk>/update/', views.BloggerUpdate.as_view(), name='blogger-update'),
    
]