from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from granola import settings
from .managers import CustomUserManager
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class ProductManager(models.Manager):

    def get_queryset(self):
        queryset = super(ProductManager, self).get_queryset()
        return queryset.select_related(
            'category'
        )


def product_upload_path(obj, file):
    return f'product/{obj.id}/{file}'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey("granola_shop.Category", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    image_main = models.ImageField(upload_to=product_upload_path, null=True)
    image_inside = models.ImageField(upload_to=product_upload_path, null=True)
    image_plate = models.ImageField(upload_to=product_upload_path, null=True)
    availability = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def get_next(self):
        next = Product.objects.filter(id__gt=self.id, availability=True).order_by('id').first()
        if next:
            return next
        else:
            return Product.objects.filter(availability=True).order_by('id').first()

    def get_previous(self):
        previous = Product.objects.filter(id__lt=self.id, availability=True).order_by('id').last()
        if previous:
            return previous
        else:
            return Product.objects.filter(availability=True).order_by('id').last()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class OrderProductManager(models.Manager):

    def get_queryset(self):
        queryset = super(OrderProductManager, self).get_queryset()
        return queryset.select_related(
            'user', 'product'
        )


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    objects = OrderProductManager()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price


class CheckoutAddress(models.Model):
    phone_message = 'Phone number must be in the following format: 0123456789'

    phone_regex = RegexValidator(
        regex=r'^0\d{9}$',
        message=phone_message
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=100, blank=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_adress = models.ForeignKey(CheckoutAddress, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email

    def get_total_price(self):
        total = 0
        for item in self.products.all():
            total += item.get_total_item_price()
        return total


@receiver(post_save, sender=CheckoutAddress)
def update_order_orderproducts(sender, **kwargs):
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            order = Order.objects.get(user=request.user, ordered=False)
            checkout_address = CheckoutAddress.objects.filter(user=request.user).last()
            order.checkout_adress = checkout_address
            order.ordered_date = timezone.now()
            order.ordered = True
            order.save()
            for order_product in OrderProduct.objects.filter(user=request.user):
                order_product.ordered = True
                order_product.save()
    else:
        request = None
