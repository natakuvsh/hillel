from random import randint
from django.core.management import BaseCommand
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from django_school.models import Course, Group, Teacher
from django_school_hw import settings


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('course_num', nargs='+', type=int)

    def handle(self, *args, **options):
        course_num = options['course_num'][0]
        for i in range(course_num):
            string = get_random_string(length=randint(3, 12), allowed_chars=settings.RANDOM_STRING_CHARS)
            course = Course(name=string, description=string, theses=string)
            course.teacher = Teacher.objects.get(id=6)
            course.save()

            with open(settings.NO_IMAGE_FILEPATH, 'rb') as f:
                data = f.read()
            course.image.save('no_image.jpg', ContentFile(data))
            group = Group.objects.filter().order_by('?').first()
            course.group.add(group)

            print(f'Successfully created Course {i}')



