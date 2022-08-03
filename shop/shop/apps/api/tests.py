from django.test import TestCase
from django.urls import reverse

from rest_framework.response import Response

from main.models import Category, Product


class APITest(TestCase):
    def setUp(self) -> None:
        Category.objects.create(name='cat 1')
        Product.objects.create(
            name='test_name',
            SKU='1234',
            category=Category.objects.get(id=1),
            price=100,
            descr='str descr',
            short_descr='str short_descr'
            )
        self.product_as_response = b'[{"id":1,"name":"test_name","SKU":"1234","price":100,"descr":"str descr","short_descr":"str short_descr","category":1}]'
        return super().setUp()
    
    def test_product_api_view(self):
        res = self.client.get(reverse('api:product'))   
        self.assertEqual(
            self.product_as_response,
            res.content)

    def test_product_filter(self):
        self.assertEqual(self.product_as_response, 
                            self.client.get(reverse('api:product'),{'id' : 1}).content)
        self.assertEqual(self.product_as_response, 
                            self.client.get(reverse('api:product'),{'category' : 1}).content)
        self.assertEqual(self.product_as_response, 
                            self.client.get(reverse('api:product'),{'name' : 'test_name'}).content)
    
    def test_create_product(self):
        self.assertEqual(
            b'{"id":2,"name":"test_name","SKU":"1234","price":100,"descr":"str descr","short_descr":"str short_descr","category":1}', 
                            self.client.post(reverse('api:product'),{
                                'name':'test_name',
                                'SKU':'1234',
                                'category':1,
                                'price':100,
                                'descr':'str descr',
                                'short_descr':'str short_descr'
                            }).content)
    
    def test_product_detail(self):
        self.assertEqual(b'{"id":1,"name":"test_name","SKU":"1234","price":100,"descr":"str descr","short_descr":"str short_descr","category":1}', 
                            self.client.get(reverse('api:prod_detail', kwargs={'pk':1})).content)


