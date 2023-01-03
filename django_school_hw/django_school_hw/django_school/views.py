from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, CreateView, View, UpdateView, TemplateView
from django_school.models import Student, Teacher, Group, Course, Category
from django_school.forms import CourseCreateForm, StudentCreateForm, StudentUpdateForm



class IndexView(ListView):
    template_name = 'index.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset.model.objects.get_prefetched_selected()


class CategoryView(ListView):
    template_name = 'course_by_cat.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Course.objects.filter(group__category=self.category)



class SearchView(IndexView):

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return self.model.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(theses__icontains=query)
            )
        return super(SearchView, self).get_queryset()



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


class StudentUpdateView(UpdateView):
    template_name = 'create_student.html'
    model = Student
    form_class = StudentUpdateForm
    pk_url_kwarg = 'student_id'
    success_url = '/'


class CourseUpdateView(UpdateView):
    template_name = 'create_course.html'
    model = Course
    form_class = CourseCreateForm
    pk_url_kwarg = 'course_id'

    def get_success_url(self):
        return reverse_lazy('add_update:course_update', args=(self.kwargs['course_id'], ))


class CourseByCat(UpdateView):
    template_name = 'course_by_cat.html'
    model = Course
    pk_url_kwarg = 'cat_id'
    success_url = '/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

