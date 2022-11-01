from django_school.models import Category

def get_all_categories(request):
    return {
        'categories': Category.objects.all()
    }