from granola_shop.models import Category, OrderProduct
from django.db.models import Sum


def get_all_categories(request):
    return {
        'categories': Category.objects.all()
    }


def get_users_cart_count(request):
    user_items = OrderProduct.objects.filter(user_id=request.user.id, ordered=False).aggregate(Sum('quantity'))['quantity__sum']
    return {
        'users_items': user_items
    }