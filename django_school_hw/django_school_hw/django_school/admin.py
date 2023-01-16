from django.contrib import admin
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django_school import models
from django_school.forms import CourseCreateForm
from django_school.models import Teacher, Group, Student, Course, Category, CustomUser, Rate, NewLot


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "theses", "teacher", "link_to_course")
    search_fields = ("id", "name")
    list_filter = ("group",)
    list_editable = ("theses", )
    readonly_fields = ("created_at", )
    form = CourseCreateForm

    def link_to_course(self, obj):
        return mark_safe(f'<a target="_blank" href={reverse_lazy("course", kwargs={"pk": obj.id})}> Open in website </a>')


class CourseAdminInline(admin.TabularInline):
    model = models.Course
    extra = 0
    fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = (CourseAdminInline, )




# Register your models here.
admin.site.register(Teacher)
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Rate)
admin.site.register(NewLot)