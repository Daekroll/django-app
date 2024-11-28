import json
import logging
import random
from pprint import pprint

from timeit import default_timer

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from rest_framework.viewsets import ModelViewSet

from .forms import ProductForm, OrderForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, reverse

from .models import Product, Order
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import ProductSerializer, OrderSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.syndication.views import Feed

logger = logging.getLogger(__name__)


def shop_index(request: HttpRequest):
    rand_num = random.randint(0, 50)
    products = [
        ('laptop', 1900),
        ('desktop', 2900),
        ('phone', 500),
    ]
    context = {
        'rand_num': rand_num,
        'products': products
    }
    logger.info(f'open this view with products: {products}')
    return render(request, 'shopapp/shop-index.html', context=context)


def product_list_view(request: HttpRequest):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'shopapp/product_list.html', context=context)


def order_view(request: HttpRequest):
    orders = Order.objects.select_related('user').prefetch_related('products').all()

    context = {
        'orders': orders
    }
    return render(request, 'shopapp/order_list.html', context=context)


def create_product(request: HttpRequest):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:product_list')
            return redirect(url)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, 'shopapp/create_product.html', context)


def new_order(request: HttpRequest):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            url = reverse('shopapp:order_list')
            return redirect(url)
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, 'shopapp/create_order.html', context)


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(is_archive=False)


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    permission_required = 'shopapp.change_product'
    model = Product
    fields = 'name', 'description', 'price', 'discount', 'count',
    template_name_suffix = '_update'

    def test_func(self):
        if self.request.user.is_superuser:
            return True

        self.object = self.get_object()

        has_edit_perm = self.request.user.has_perm("shopapp.change_product")
        created_by_current_user = self.object.created_by == self.request.user
        return has_edit_perm and created_by_current_user

    def get_success_url(self):
        return reverse('shopapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_archive = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'description', 'price', 'discount', 'count',
    success_url = reverse_lazy('shopapp:product_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class OrderListView(ListView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    queryset = (Order.objects.select_related('user').prefetch_related('products'))


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'address', 'comment', 'user', 'products',
    template_name = 'shopapp/order_update.html'

    def get_success_url(self):
        return reverse('shopapp:order_detail', kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


@user_passes_test(lambda u: u.is_staff, login_url='/shop/')
def order_list_json_view(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.select_related('user').prefetch_related('products').all()
    data = {
        'orders': [
            {'id': order.pk, 'address': order.address, 'promocode': order.promocode, 'user_id': order.user.pk,
             'products_id': [pk.pk if order.products else None for pk in order.products.all()]} for order in
            orders]}
    return JsonResponse(data)


class ProductApiViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name', 'price']
    ordering_fields = ['price', 'created_by']
    ordering = ['price']


class OrderApiViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('address',
                        'comment',
                        'create_date',
                        'user',
                        'promocode',
                        'products',)
    ordering_fields = ['address', 'create_date']
    ordering = ['address']


class LatestProductsFeed(Feed):
    title = 'Продукты'
    link = reverse_lazy('shopapp:product_list')
    description = "Обновления последних продуктов."

    def items(self):
        return Product.objects.filter(is_archive=False).order_by('create_date')

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:50]


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_pk = self.kwargs.get('pk')
        orders = Order.objects.filter(user=user_pk).prefetch_related('user', 'products')
        return orders

    def get_context_data(self, **kwargs):
        user_pk = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")

        context = super().get_context_data(**kwargs)
        context['current_user'] = user
        return context


class UserOrderJSONView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("Пользователь не найден")
        data = cache.get(user.pk)
        if data is None:
            orders = Order.objects.filter(user=user).prefetch_related('user', 'products').order_by('pk')

            data = [
                {'pk': order.pk,
                 'user': order.user.username,
                 'address': order.address,
                 'products': [product.name for product in order.products.all()]}
                for order in orders]
            cache.set(pk, data, timeout=300)
        return JsonResponse(data=data, safe=False)
