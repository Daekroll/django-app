from django.core.management import BaseCommand
from shopapp.models import Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Crate order')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            address="Lenina d 6",
            comment="kod 123",
            user=user,

        )

        self.stdout.write(self.style.SUCCESS(f'Crated order: {order}'))
