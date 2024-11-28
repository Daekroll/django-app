from django.core.management import BaseCommand
from shopapp.models import Product, Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        order = Order.objects.first()
        if not order:
            self.stdout.write('no order found')
            return
        products = Product.objects.all()

        for product in products:
            order.products.add(product)
            self.stdout.write(f'В заказ {order} добавлены {product.name}')

        order.save()

        self.stdout.write('Order update...')
