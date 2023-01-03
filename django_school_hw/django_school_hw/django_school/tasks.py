import datetime
from django_school_hw.celery import app
from django.core.mail import send_mail
from django_school.models import Student, Course


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