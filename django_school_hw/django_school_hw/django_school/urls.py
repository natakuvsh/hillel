from django.urls import path
from django_school import views


urlpatterns = [
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<int:course_id>/edit/', views.CourseUpdateView.as_view(), name='course_update'),
    path('student/create/', views.StudentCreateView.as_view(), name='student_create'),
    path('student/<int:student_id>/edit/', views.StudentUpdateView.as_view(), name='student_update'),
]