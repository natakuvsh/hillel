from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
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


class CourseCreateView(TemplateView):
    template_name = 'create_course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView,self).get_context_data(**kwargs)
        context['form'] = CourseCreateForm()

        return context

    def post(self, request):
        form = CourseCreateForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.create_course()
            return redirect('/')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class StudentCreateView(TemplateView):
    template_name = 'create_student.html'

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['form'] = StudentCreateForm()

        return context

    def post(self, request):
        form = StudentCreateForm(data=request.POST)

        if form.is_valid():
            form.create_student()
            return redirect('/')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

       
