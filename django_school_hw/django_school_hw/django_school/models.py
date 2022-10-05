from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    group = models.ForeignKey("django_school.Group", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name},{self.age} years old, {self.email}'


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True)
    group = models.ForeignKey("django_school.Group", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name},{self.age} years old, {self.email}'
