from django.contrib.auth.models import AbstractUser
from django.db import models


def course_upload_path(obj, file):
    return f'course/{obj.name}/{file}'


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
    pass


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):

    def get_queryset(self):
        queryset = super(ProductManager, self).get_queryset()
        return queryset.filter(teacher__isnull=False)

    def get_prefetched_selected(self):
        return self.get_queryset().select_related(
                'teacher'
            ).prefetch_related(
                'group'
            )


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    theses = models.TextField()
    group = models.ManyToManyField("Group")
    image = models.ImageField(upload_to=course_upload_path, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    group = models.ManyToManyField("Group")

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    pass