import json
from granola_shop import context_processing
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, DetailView, TemplateView, UpdateView
from granola_shop.forms import RegistrationForm, ContactForm, CheckoutForm
from granola_shop.models import Product, Order, OrderProduct, Category, CheckoutAddress
from django.utils import timezone
# Create your views here.


class IndexView(ListView):
    template_name = 'index.html'
    model = Product


class ShopView(ListView):
    template_name = 'shop.html'
    model = Product

    def get_queryset(self):
        queryset = super(ShopView, self).get_queryset()
        return queryset.model.objects.all()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def post(self, request, *args, **kwargs):

        response_data = {}
        user_id = request.user.id
        user = get_user_model().objects.filter(id=user_id)
        last_name = request.POST.get('last_name')
        if last_name:
            user.update(last_name=last_name)
        first_name = request.POST.get('first_name')
        if first_name:
            user.update(first_name=first_name)

        response_data['success'] = 'Profile updated succesfully'
        return HttpResponseRedirect('/profile/', json.dumps(response_data), content_type="application/json")


class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/profile/')
        else:
            return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user = authenticate(
            self.request,
            username=user.email,
            password=form.cleaned_data['password']
        )
        login(request=self.request, user=user)
        return super(RegistrationView, self).form_valid(form)


class CategoryView(ListView):
    template_name = 'product_category.html'
    model = Product

    def get_queryset(self):
        products = Product.objects.filter(category=self.kwargs['category_id'], availability=True)
        return products


class ProductDetailView(DetailView):
    template_name = 'product.html'
    model = Product

    def post(self, request, *args, **kwargs):
        response_data = {}

        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        user = request.user

        product = Product.objects.get(id=product_id)

        if product.quantity >= int(quantity):
            if OrderProduct.objects.filter(user=user, product=product, ordered=False).exists():
                order_product = OrderProduct.objects.get(user=user, product=product, ordered=False)
                order_product.quantity += int(quantity)
                order_product.save()
            else:
                order_product = OrderProduct.objects.create(user=user, product=product, quantity=quantity, ordered=False)
            try:
                order = Order.objects.get(user=user, ordered=False)
                order.products.add(order_product)
            except ObjectDoesNotExist:
                ordered_date = timezone.now()
                order = Order.objects.create(user=user, ordered_date=ordered_date, ordered=False)
                order.products.add(order_product)
                response_data['success'] = 'Updated cart successfully!'
        else:
            response_data['quantity_error'] = 'Not enough stock'

        return HttpResponse(json.dumps(response_data), content_type="application/json")


class ReduceQuantityView(View):

    def post(self, request, *args, **kwargs):

        response_data = {}
        product_id = request.POST.get('product_id')
        user = request.user

        product = Product.objects.get(id=product_id)
        if OrderProduct.objects.filter(user=user, product=product, ordered=False).exists():
            order_product = OrderProduct.objects.get(user=user, product=product, ordered=False)
            current_quantity = order_product.quantity
            if current_quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order_product.delete()
            response_data['success'] = 'Update lot successful!'
        else:
            return redirect("cart")
        return HttpResponse(json.dumps(response_data), content_type="application/json")


class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    model = OrderProduct

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CartView, self).get_context_data()
        order = OrderProduct.objects.filter(user=self.request.user, ordered=False)
        total_price = 0
        for order_item in order:
            total_price += order_item.get_total_item_price()

        context['order'] = order
        context['total'] = total_price
        return context


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'checkout.html'
    model = CheckoutAddress
    form_class = CheckoutForm
    success_url = reverse_lazy('thank_you')

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data()
        order = OrderProduct.objects.filter(user=self.request.user, ordered=False)
        total_price = 0
        for order_item in order:
            total_price += order_item.get_total_item_price()

        context['order_items'] = order
        context['total'] = total_price
        return context

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user = self.request.user
        first_name = self.request.POST.get('first_name')
        if first_name:
            form.first_name = first_name
        else:
            form.first_name = self.request.user.first_name
        last_name = self.request.POST.get('last_name')
        if last_name:
            form.last_name = last_name
        else:
            form.last_name = self.request.user.last_name
        form.save()

        return super(CheckoutView, self).form_valid(form)


class ThankYouView(TemplateView):
    template_name = 'thank_you.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(ContactView, self).form_valid(form)




