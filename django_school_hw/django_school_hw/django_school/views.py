import json

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, FormView, CreateView, UpdateView, TemplateView, DetailView
from django_school.models import Student, Course, Category, NewLot
from django_school.forms import CourseCreateForm, StudentCreateForm, StudentUpdateForm, CreateLotForm, UpdateLotForm, CloseLotForm


@method_decorator(cache_page(1000, key_prefix='index'), 'get')
class IndexView(ListView):
    template_name = 'index.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        queryset = super(IndexView, self).get_queryset()
        return queryset.model.objects.get_prefetched_selected()


@method_decorator(cache_page(500, key_prefix='category'), 'get')
class CategoryView(ListView):
    template_name = 'course_by_cat.html'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Course.objects.filter(group__category=self.category)


class SearchView(IndexView):
    template_name = 'search.html'
    context_object_name = 'search_results'

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
        form.send_email()
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
        return reverse_lazy('add_update:course_update', args=(self.kwargs['course_id'],))


class CourseByCat(UpdateView):
    template_name = 'course_by_cat.html'
    model = Course
    pk_url_kwarg = 'cat_id'
    success_url = '/'


@method_decorator(cache_page(100, key_prefix='profile'), 'get')
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


class CourseDetailView(DetailView):
    template_name = 'course.html'
    model = Course


class ApiTeachersView(TemplateView):
    template_name = 'api_ui.html'



class LotsView(ListView):
    template_name = 'lots.html'
    model = NewLot

    def get_context_data(self, **kwargs):
        context = super(LotsView, self).get_context_data(**kwargs)
        context['form'] = CreateLotForm()
        return context


class CreateLotView(FormView):
    template_name = 'includes/create_lot.html'
    form_class = CreateLotForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creator = self.request.user
        instance.save()
        return JsonResponse({'redirect_url': reverse_lazy('lots',)})


class LotUpdateView(UpdateView):
    template_name = 'lot.html'
    model = NewLot
    form_class = UpdateLotForm
    pk_url_kwarg = 'lot_id'

    def post(self, request, *args, **kwargs):
        response_data = {}

        bid = request.POST.get('bid')
        id = request.POST.get('id')

        lot = NewLot.objects.get(id=id)
        if float(bid) <= lot.bid:
            response_data['error'] = 'Bid should be greater than current one!'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        lot.bid = bid
        lot.save()
        response_data['success'] = 'Update lot successful!'
        response_data['bid'] = lot.bid

        return HttpResponse(json.dumps(response_data), content_type="application/json")


class LotDetailView(DetailView):
    template_name = 'lot.html'
    model = NewLot

    def get_context_data(self, **kwargs):
        context = super(LotDetailView, self).get_context_data(**kwargs)
        context['form'] = UpdateLotForm()
        return context


class LotCloseView(UpdateView):
    template_name = 'includes/update_lot.html'
    model = NewLot
    form_class = CloseLotForm
    pk_url_kwarg = 'lot_id'
    success_url = reverse_lazy('lots')


    def post(self, request, *args, **kwargs):
        response_data = {}
        id = request.POST.get('id')
        if request.POST.get('closed') == 'true':
            closed = True
        lot = NewLot.objects.get(id=id)

        lot.closed = closed
        lot.save()
        response_data['success'] = 'Update lot successful!'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
