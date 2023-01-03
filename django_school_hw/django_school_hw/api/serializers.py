from rest_framework import serializers
from django_school.models import Student, Teacher


class NameItSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.IntegerField()


class StudentSerializer(serializers.ModelSerializer):

    applied_course = NameItSerializer(source='course', read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    group = NameItSerializer(many=True, read_only=True)
    group_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    group = NameItSerializer(many=True, read_only=True)
    group_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'

