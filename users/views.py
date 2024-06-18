from django.shortcuts import render, redirect
import random
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from users.forms import UsersRegisterForm, UsersForm
from users.models import User


class UsersListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return User.objects.filter(Q(first_name__icontains=query) | Q(email__icontains=query))
        else:
            return User.objects.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'
    context_object_name = 'user'


class LoginView(BaseLoginView):
    template_name = 'user/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UsersRegisterForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Добро пожаловать на наш сайт!',
            message='Поздравляем с регистрацией на нашей платформе!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('user:user_list')
    form_class = UsersForm

    def get_object(self, queryset=None):
        return self.request.user


def generate_password(request):
    password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш новый пароль: {password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )

    request.user.set_password(password)
    request.user.save()
    return redirect(reverse('user:login'))
