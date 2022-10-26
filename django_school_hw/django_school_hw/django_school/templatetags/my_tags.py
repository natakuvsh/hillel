from django import template
from django_school.models import Course, Student
from django.db.models import Count


register = template.Library()


@register.filter
def check_even_num(num_list):
    even_num_list = [num for num in num_list if isinstance(num, int) and (num % 2 == 0)]
    return even_num_list


@register.filter
def count_words(string):
    return len(string.split())


@register.inclusion_tag('includes/course_list.html')
def get_popular_courses():
    return {
        'course_list': Course.objects.get_prefetched_selected().annotate(popular=Count('student')).order_by('-popular')[:5]
    }

