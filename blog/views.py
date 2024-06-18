from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.forms import BlogForm
from blog.models import Blog
from distribution.models import Distribution, DistributionClient


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_stat = form.save()
            new_stat.slug = slugify(new_stat.title)
            new_stat.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blog.change_blog'

    def form_valid(self, form):
        if form.is_valid():
            new_stat = form.save()
            new_stat.slug = slugify(new_stat.title)
            new_stat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blog'


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_feature=True)
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['distribution_count'] = Distribution.objects.all().count()
        context_data['active_distribution_count'] = Distribution.objects.filter(
            status=Distribution.status_started).count()
        context_data['count_unique_distribution_client'] = DistributionClient.objects.all().count()
        context_data['blog_list'] = Blog.objects.all().order_by('?')[:3]
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object
