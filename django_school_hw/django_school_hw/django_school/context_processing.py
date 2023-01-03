from django_school.models import Course

def get_all_courses(request):
    return {
        'courses': Course.objects.all()
    }