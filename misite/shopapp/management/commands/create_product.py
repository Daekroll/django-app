from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_names = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        for products_name, price in products_names:
            product, created = Product.objects.get_or_create(name=products_name,price=price)
            self.stdout.write(f"Created product {product.name}")
        self.stdout.write(self.style.SUCCESS("Products created"))
