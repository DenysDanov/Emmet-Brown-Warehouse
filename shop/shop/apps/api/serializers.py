from rest_framework import serializers
from main.models import Product, Category
from django.contrib.auth.models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'