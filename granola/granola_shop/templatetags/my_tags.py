from django import template
from granola_shop.models import Product, Category

register = template.Library()


@register.inclusion_tag('includes/product_list.html')
def get_related_products():
    return {
        'product_list': Product.objects.filter(availability=True).order_by('?')[:3]
    }

@register.simple_tag()
def get_name_by_cat_id(cat_id):
    return Category.objects.get(id=cat_id)


@register.inclusion_tag('includes/products_index.html')
def get_most_stock_products():
    return {
        'product_list': Product.objects.filter(availability=True).order_by('-quantity')[:4]
    }