import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse


from shopapp.models import Order, Product


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='TestUser', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.product = Product.objects.create(
            name='testproduct',
            price='100',
            created_by=self.user
        )
        self.order = Order.objects.create(
            address='Moscow',
            comment='test',
            user=self.user,
            promocode='ROTPER24/7'
        )
        self.order.products.add(self.product)

    def tearDown(self):
        self.order.delete()
        self.product.delete()

    def test_order_details(self):
        response = self.client.get(reverse('shopapp:order_detail', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context["object"].pk, self.order.pk)


class OrdersExportTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='TestUser', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.is_staff = True
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.login(**self.credentials)
        self.product = Product.objects.create(
            name='testproduct',
            price='100',
            created_by=self.user
        )
        self.order = Order.objects.create(
            address='Moscow',
            comment='test',
            user=self.user,
            promocode='ROTPER24/7'
        )
        self.order.products.add(self.product)
        self.client.login(**self.credentials)

    def test_content_response(self):
        response = self.client.get(reverse('shopapp:orders_json'))
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('orders')[0].get('address'), 'Moscow')
        self.assertEqual(data.get('orders')[0].get('promocode'), 'ROTPER24/7')
        self.assertEqual(data.get('orders')[0].get('user_id'), self.user.pk)
        self.assertEqual(data.get('orders')[0].get('products_id'), [self.product.pk])


class OrdersExportFixturesTestCase(TestCase):
    fixtures = [
        'fixtures_users.json',
        'fixtures_products.json',
        'fixtures_orders.json',
    ]

    def setUp(self):
        self.user = User.objects.filter(username='admin')[0]
        self.client.force_login(self.user)
        self.products = Product.objects.select_related('user').all()
        self.orders = Order.objects.select_related('user').prefetch_related('products').all()

    def test_get_product_view(self):
        verification_data = {
            "orders": [
                {
                    "id": 1,
                    "address": "Lenina 10",
                    "promocode": "",
                    "user_id": 1,
                    "products_id": [5, 7]
                },
                {
                    "id": 2,
                    "address": "lenina 10",
                    "promocode": "ROTPER24/7",
                    "user_id": 1,
                    "products_id": [8]
                },
                {
                    "id": 3,
                    "address": "lenina 10",
                    "promocode": "ROTPER24/7",
                    "user_id": 1,
                    "products_id": [5, 7, 8]
                }
            ]
        }
        response = self.client.get(reverse('shopapp:orders_json'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, verification_data)
