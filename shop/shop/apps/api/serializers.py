from rest_framework import serializers
from main.models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'SKU',
            'price',
            'descr',
            'short_descr',
            'category',
        )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name'
        )