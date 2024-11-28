from csv import DictReader
from io import TextIOWrapper

from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path

from .models import Product, Order
from .forms import CSVImportForm


class OrderInLine(admin.TabularInline):
    model = Product.orders.through


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archive=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(is_archive=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [
        mark_archived,
        mark_unarchived,
    ]
    inlines = [
        OrderInLine,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "is_archive"
    list_display_links = "pk", "name"
    ordering = "pk", "-name"
    search_fields = "name", "price", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description")
        }),
        ("Price options", {
            "fields": ("price", "discount"),
        }),
        ("Extra options", {
            "fields": ("is_archive",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'is_archive' is for soft delete",
        })
    ]

    @classmethod
    def description_short(cls, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changelist.html"
    inlines = [
        ProductInLine,
    ]
    list_display = "pk", "address", "comment", "user_verbose",

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        scv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )
        reader = DictReader(scv_file)

        for row in reader:
            user = get_object_or_404(User, pk=int(row.get('user')))
            products = [get_object_or_404(Product, pk=int(pk)) for pk in list(row.get('products')) if pk.isdigit()]
            order = Order(
                address=row.get('address'),
                comment=row.get('comment'),
                user=user,
                promocode=row.get('promocode'),
            )
            order.save()
            order.products.add(*products)

        return redirect('..')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-order-csv/',
                 self.import_csv,
                 name='import-order-csv')
        ]
        return new_urls + urls

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv/",
                self.import_csv,
                name="import-orders-csv"
            )
        ]
        return new_urls + urls
