from django import template

register = template.Library()


@register.filter
def check_even_num(num_list):
    even_num_list = [num for num in num_list if isinstance(num, int) and (num % 2 == 0)]
    return even_num_list


@register.filter
def count_words(string):
    return len(string.split())