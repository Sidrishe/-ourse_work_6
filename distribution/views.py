from django.shortcuts import render

import datetime
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Blog
from distribution.forms import DistributionForm, MessageForm, DistributionClientForm
from distribution.models import Distribution, Message, DistributionClient


class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['distribution_count'] = Distribution.objects.all().count()
        context_data['active_distribution_count'] = Distribution.objects.filter(
            status=Distribution.status_started).count()
        context_data['count_unique_distribution_client'] = DistributionClient.objects.all().count()
        context_data['blog_list'] = Blog.objects.all().order_by('?')[:3]
        return context_data


class DistributionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Distribution
    template_name = 'distribution/distribution_detail.html'
    context_object_name = 'distribution'
    permission_required = 'distribution.view_distribution'


class DistributionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Distribution
    form_class = DistributionForm
    permission_required = 'distribution.add_distribution'
    success_url = reverse_lazy('distribution:distribution_list')

    def form_valid(self, form):

        """
        Проверка текущей даты, с датой начала и окончания рассылки.
        """
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            day_today = datetime.date.today()
            if self.object.start_time <= day_today < self.object.end_time:
                self.object.status = 'started'
                mail = self.object.message
                users = self.object.distribution_client.all()
                for user in users:
                    send_mail(
                        subject=mail.subject,
                        message=mail.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                self.object.datatime = day_today
            elif day_today > self.object.end_time:
                self.object.status = 'completed'
            self.object.save()
            return super().form_valid(form)


class DistributionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Distribution
    form_class = DistributionForm
    permission_required = 'distribution.change_distribution'
    success_url = reverse_lazy('distribution:distribution_list')

    def form_valid(self, form):

        """
        Проверка текущей даты, с датой начала и окончания рассылки.
        """
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            day_today = datetime.date.today()
            if self.object.start_time <= day_today < self.object.end_time:
                self.object.status = 'started'
                mail = self.object.message
                users = self.object.distribution_client.all()
                for user in users:
                    send_mail(
                        subject=mail.subject,
                        message=mail.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email]
                    )
                self.object.datatime = day_today
            elif day_today > self.object.end_time:
                self.object.status = 'completed'
            self.object.save()
            return super().form_valid(form)


class DistributionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Distribution
    success_url = reverse_lazy('distribution:distribution_list')
    permission_required = 'distribution.delete_distribution'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('distribution:distribution_list')
    permission_required = 'distribution.add_message'


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('distribution:distribution_detail')
    permission_required = 'distribution.delete_message'


class DistributionClientListView(LoginRequiredMixin, ListView):
    model = DistributionClient
    template_name = 'distribution/distribution_client_list.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['client_list'] = self.get_queryset()
        return context_data


class DistributionClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = DistributionClient
    template_name = 'distribution/distribution_client_form.html'
    form_class = DistributionClientForm
    success_url = reverse_lazy('distribution:distribution_client_list')
    permission_required = 'distribution.add_distribution_client'


class DistributionClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DistributionClient
    template_name = 'distribution/distribution_client_form.html'
    form_class = DistributionClientForm
    success_url = reverse_lazy('distribution:distribution_client_list')
    permission_required = 'distribution.change_distribution_client'


class DistributionClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DistributionClient
    template_name = 'distribution/distribution_client_confirm_delete.html'
    success_url = reverse_lazy('distribution:distribution_client_list')
    permission_required = 'distribution.delete_distribution_client'
