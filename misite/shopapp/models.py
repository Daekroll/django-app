import decimal

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=2000, blank=True)
    price = models.DecimalField(default=decimal.Decimal('0.00'), max_digits=10, decimal_places=2, blank=False,
                                null=False)
    discount = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    is_archive = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='products')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        return f"product {self.name}"

    def get_absolute_url(self):
        return reverse("shopapp:product_detail", kwargs={"pk": self.pk})

    # def description_short(self) -> str:
    #     if len(self.description) < 48:
    #         return self.description
    #     return self.description[:48] + '...'


class Order(models.Model):
    address = models.CharField(max_length=255, blank=False, null=False)
    comment = models.TextField(max_length=500, blank=True, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='orders')
    promocode = models.CharField(max_length=10, blank=True, null=False)
    products = models.ManyToManyField(to=Product, related_name='orders')

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f"delivery address {self.address}"
