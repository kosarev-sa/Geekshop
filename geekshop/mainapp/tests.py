from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    status_code_success = 200

    def setUp(self) -> None:
        category = ProductCategory.objects.create(name="Test")
        Product.objects.create(category=category, name='product_test', price=1000)
        Product.objects.create(category=category, name='product_test1', price=500)
        self.client = Client()

    def test_product_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_products_basket(self):
        response = self.client.get('/users/profile/')
        self.assertEqual(response.status_code, 302)

    def tearDown(self) -> None:
        pass
