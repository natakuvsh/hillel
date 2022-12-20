from random import randint

from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from django_school.models import Course, Group, Category, Student
from django_school_hw import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('students_num', nargs='+', type=int)

    def handle(self, *args, **options):
        student_num = options['students_num'][0]
        for i in range(student_num):
            string = get_random_string(length=randint(3, 12), allowed_chars=settings.RANDOM_STRING_CHARS)
            student = Student(name=string, email=string + '@gmail.com', surname=string)
            student.save()
            group = Group.objects.filter().order_by('?').first()
            student.group.add(group)

            print(f'Successfully created Student {i}')