from django.views.decorators.cache import cache_page
from blog.apps import BlogConfig
from django.urls import path
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('blog/view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),

]