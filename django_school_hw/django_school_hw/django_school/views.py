from django.views.generic import ListView
from django_school.models import Student, Teacher, Group, Course


class IndexView(ListView):
    template_name = 'index.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset.select_related('teacher').prefetch_related('group')


       
