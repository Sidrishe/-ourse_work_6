from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=250, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=100, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=100, **NULLABLE, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')
    comment = models.TextField(**NULLABLE, verbose_name='Описание')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
