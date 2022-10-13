from django.db import models


def course_upload_path(obj, file):
    return f'course/{obj.name}/{file}'


class NameAgeEmail(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    group = models.ForeignKey("django_school.Group", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}   {self.email}'


class Teacher(NameAgeEmail):
   pass


class Student(NameAgeEmail):
    pass


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductManager(models.Manager):

    def get_queryset(self):
        queryset = super(ProductManager, self).get_queryset()
        return queryset.filter(teacher__isnull=False)


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey("Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    theses = models.TextField()
    group = models.ManyToManyField("Group")
    image = models.ImageField(upload_to=course_upload_path, null=True)

    objects = ProductManager()

    def __str__(self):
        return self.name



