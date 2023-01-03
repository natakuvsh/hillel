from django.urls import path
from rest_framework import routers
from api import views
from api.auth import CustomAuthToken

router = routers.SimpleRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'teachers', views.TeacherViewSet)

urlpatterns = [
    path('get-token/', CustomAuthToken.as_view(), name='get_token')
] + router.urls