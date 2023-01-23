from django.contrib import admin
from granola_shop import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "price", "category", "availability", "link_to_product")
    search_fields = ("id", "name")
    list_editable = ("availability",)
    list_filter = ("category",)
    readonly_fields = ("created_at","updated_at" )

    def link_to_product(self, obj):
        return mark_safe(f'<a target="_blank" href={reverse_lazy("product", kwargs={"pk": obj.id})}> Open in website </a>')


class OrderAdminInline(admin.TabularInline):
    model = models.Order
    extra = 0
    fields = ('products', 'ordered' )


class CheckoutAddressAdminInline(admin.TabularInline):
    model = models.CheckoutAddress
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInline, CheckoutAddressAdminInline)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Category)
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.OrderProduct)
admin.site.register(models.Order)
admin.site.register(models.CheckoutAddress)