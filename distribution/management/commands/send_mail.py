import datetime
import schedule
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from distribution.models import Distribution


def sendmail(message, user):
    """
    Отправка письма клиенту
    """
    send_mail(
        subject=message.subject,
        message=message.body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def frequency_check(distribution):
    """
    Проверка периодичности оправки сообщений
    """
    next_try = None
    if distribution.frequency == 'daily':
        next_try = distribution.datetime + datetime.timedelta(days=1)
    elif distribution.frequency == 'weekly':
        next_try = distribution.datetime + datetime.timedelta(days=7)
    elif distribution.frequency == 'monthly':
        next_try = distribution.datetime + datetime.timedelta(days=30)
    return next_try


def start_check(distribution):
    """
    Проверка даты начала рассылки для ее активации
    """
    if distribution.start_time == datetime.date.today():
        for user in distribution.distribution_client.all():
            sendmail(distribution.message, user)
            distribution.status = 'started'
            distribution.save()


def finish_check(distribution):
    """
    Проверка даты окончания рассылки для ее отключения
    """
    for user in distribution.distribution_client.all():
        sendmail(distribution.message, user)
        distribution.datetime = datetime.date.today()
    if distribution.end_time == datetime.date.today():
        distribution.status = 'completed'
    distribution.save()


def distribution_check():
    """
    Проверка всей рассылки на сроки этой рассылки и отправляет сообщения
    """
    for distribution in Distribution.objects.all():
        try:
            if datetime.date.today() == frequency_check(distribution):
                if distribution.status == 'created':
                    start_check(distribution)
                elif distribution.status == 'started':
                    finish_check(distribution)
            distribution.attempt = True
        except:
            distribution.feedback = 'Ошибка рассылки'
            distribution.attempt = False


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Запуск бесконечного цикла, для проверки рассылок и отправки сообщений
        """
        schedule.every().day.at("10:00").do(distribution_check)

        while True:
            schedule.run_pending()
