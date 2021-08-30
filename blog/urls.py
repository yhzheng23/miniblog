from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/',views.BlogListView.as_view(),name='blogs'),
    path('bloggers/',views.BloggerListView.as_view(),name='bloggers'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(),name='blog-detail'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(),name='blogger-detail'),

    path('blog/create/', views.BlogCreate.as_view(), name='blog-create'),
    path('blogger/update/', views.BloggerUpdate.as_view(), name='blogger-update'),

    path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog_comment'),
    
]