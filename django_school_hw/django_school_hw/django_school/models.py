from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def course_upload_path(obj, file):
    return f'course/{obj.name}/{file}'

class CourseManager(models.Manager):

    def get_queryset(self):
        queryset = super(CourseManager, self).get_queryset()
        return queryset.filter(teacher__isnull=False)

    def get_prefetched_selected(self):
        return self.get_queryset().select_related(
            'teacher'
        ).prefetch_related(
            'group'
        )


class StudentManager(models.Manager):

    def get_queryset(self):
        queryset = super(StudentManager, self).get_queryset()
        return queryset

    def get_prefetched_selected(self):
        return self.get_queryset().select_related(
            'course'
        ).prefetch_related(
            'group'
        )


class NameAgeEmail(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    group = models.ManyToManyField("django_school.Group")

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}   {self.email}'


class Teacher(NameAgeEmail):
    pass


class Student(NameAgeEmail):
    surname = models.CharField(max_length=255, unique=True, null=False)
    course = models.ForeignKey("django_school.Course", on_delete=models.SET_NULL, null=True)

    objects = StudentManager()


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    theses = models.TextField()
    group = models.ManyToManyField("Group")
    image = models.ImageField(upload_to=course_upload_path, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = CourseManager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    group = models.ManyToManyField("Group")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    pass


@receiver(post_save, sender=Course)
def delete_cache(**kwargs):
    from django.core.cache import cache
    cache.clear()
    print('Deleted cache')


@receiver(post_delete, sender=Course)
def delete_cache(**kwargs):
    from django.core.cache import cache
    cache.clear()
    print('Deleted cache')

