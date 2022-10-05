from django.views.generic import TemplateView
from django_school.models import Student, Teacher, Group


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Show all students in database
        students = Student.objects.all()
        print(students)

        # Show all teachers in database
        teachers = Teacher.objects.all()
        print(teachers)

        # Show all groups in database
        groups = Group.objects.all()
        print(groups)

        # Show all students with the age > 20
        students_age = Student.objects.filter(
            age__gt=20
        )
        print(students_age)

        # Show all students with "@gmail.com" email
        students_email = Student.objects.filter(
            email__endswith='gmail.com'
        )
        print(students_email)

        # Show all students for group
        for group in Group.objects.all():
            students_for_group = Student.objects.filter(
                group_id__name=group
            )
            if students_for_group:
                print (f'In {group} group there are {students_for_group}')

        # Show students for teacher
        for group in Group.objects.all():
            students_for_group = Student.objects.filter(
                group_id__name=group
            )
            teachers_for_group = Teacher.objects.filter(
                group_id__name=group
            )
            if students_for_group and teachers_for_group:
                print(f'{students_for_group} in {teachers_for_group} group')

        # Show students for teacher, who has age > 20
        for group in Group.objects.all():
            students_for_group = Student.objects.filter(
                group_id__name=group
            )
            teachers_for_group = Teacher.objects.filter(
                group_id__name=group, age__gt=20
            )
            if students_for_group and teachers_for_group:
                print(f'{students_for_group} in {teachers_for_group} group')

