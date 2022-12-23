"""django_school_hw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django_school import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('category/<int:category_id>', views.CategoryView.as_view(), name='categories'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', include(('django_school.urls', 'django_school'), namespace='add_update')),
    path('api/v1/', include(('api.urls', 'api'), namespace='api')),
    path('api/teachers', views.ApiTeachersView.as_view(), name='api_ui'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('course/<int:pk>/', views.CourseDetailView.as_view(), name='course')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
