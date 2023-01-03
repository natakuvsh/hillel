from rest_framework.viewsets import ModelViewSet
from api.serializers import StudentSerializer, NameItSerializer, TeacherSerializer
from django_school.models import Student, Group, Teacher


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.none()

    def get_queryset(self):
        return Student.objects.get_prefetched_selected()


class GroupViewSet(ModelViewSet):
    serializer_class = NameItSerializer
    queryset = Group.objects.all()


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
