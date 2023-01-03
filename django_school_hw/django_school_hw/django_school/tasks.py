import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.templatetags import rest_framework

from django_school_hw.celery import app
from django.core.mail import send_mail
from django_school.models import Student, Course, CustomUser


@app.task
def send_emails_new_course(name, description):
    emails = Student.objects.all().values_list('email', flat=True)
    message = f'''
    Our new {name} course is started.
    {description}
    Take a look!
    '''
    for email in emails:
        send_mail(
            subject='Take a look at our new course!',
            from_email='no-reply@info.com',
            message=message,
            recipient_list=[email]
        )


@app.task
def send_emails_beat():
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    new_courses = Course.objects.filter(created_at__gte=date_from).values_list('name', flat=True)
    emails = Student.objects.all().values_list('email', flat=True)
    message = f'''
Our new  {','.join(new_courses)}course is started.
Take a look!
    '''
    for email in emails:
        send_mail(
            subject='Take a look at our new course!',
            from_email='no-reply@info.com',
            message=message,
            recipient_list=[email]
        )


@app.task
def create_token_beat():
    users = get_user_model().objects.all()
    for user in users:
        try:
            Token.objects.get(user=user).delete()
        except ObjectDoesNotExist:
            pass
        Token.objects.create(user=user)

