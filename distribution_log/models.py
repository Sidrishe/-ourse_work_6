from django.db import models

import datetime
from distribution.models import Distribution
from users.models import User


class DistributionLog(models.Model):
    status_success = 'success'
    status_failure = 'failure'

    statuses = (
        (status_success, 'success'),
        (status_failure, 'failure')
    )

    sent_time = models.DateTimeField(auto_now_add=True, verbose_name='Отправка')
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=statuses, default=status_success, verbose_name='Статус')

    def __str__(self):
        return f'{self.sent_time}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
