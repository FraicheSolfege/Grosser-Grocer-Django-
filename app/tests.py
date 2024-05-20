from django.test import TestCase
from app.models import *
# Create your tests here.

class TestCse(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name='test', price=100)
        self.assertEqual(product.name, 'test')
        self.assertEqual(product.price, 100)