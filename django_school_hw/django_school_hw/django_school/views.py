from django.db.models import Q
from django.views.generic import ListView, FormView, CreateView
from django_school.models import Student, Teacher, Group, Course
from django_school.forms import CourseCreateForm, StudentCreateForm


class IndexView(ListView):
    template_name = 'index.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset.model.objects.get_prefetched_selected()


class SearchView(IndexView):

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return self.model.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(theses__icontains=query)
            )
        return super(SearchView,self).get_queryset()


class StudentCreateView(CreateView):
    template_name = 'create_student.html'
    form_class = StudentCreateForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(StudentCreateView, self).form_valid(form)


class CourseCreateView(FormView):
    template_name = 'create_course.html'
    form_class = CourseCreateForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
