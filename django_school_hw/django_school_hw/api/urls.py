from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views


router = routers.SimpleRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'teachers', views.TeacherViewSet)

urlpatterns = [

] + router.urls