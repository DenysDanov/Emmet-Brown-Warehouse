import redis

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from main.models import Product, Category
from main.cart import Cart
from main.service import ReadOnly
from .serializers import CategorySerializer, ProductSerializer


r = redis.Redis()
user_cart_store = redis.Redis(host='127.0.0.1', port=6379, db = 1)


class ProductApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id']
    permission_classes = [IsAdminUser|ReadOnly]

class ProductApiUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser|ReadOnly]

class ProductApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser|ReadOnly]

class CategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartApiOrder(APIView):
    def post(self, request):
        Cart(r, request).order()
        return Response({'success' : True})

class CartApiView(APIView):
    
    permission_classes = [IsAdminUser|ReadOnly]

    def get(self, request):
        cart = Cart(r, user_cart_store, request).getproducts()
    
        return Response({
            'main' :  cart
            })
    def post(self, request):
        try:
            prod_id = request.POST.get('prod_id')
            quantity = request.POST.get('quantity')
            Cart(r, request).addproduct(prod_id, quantity).save()
        except Exception as e:
            return Response({
            'main' :  {
                'message' : f'Error {e} occured',
                'error' : True  
                }
            })
        else:
            return Response({
            'main' :  {
                'message' : f'Product was successfully added to cart',
                'error' : False  
                }
            })   
            

    def delete(self,request):
        try:
            cart = Cart(r,request, id=request.data.get('cart_id')).delete()
        except Exception as e:
            return Response({
            'main' :  {
                'message' : f'Error {e} occured',
                'error' : True  
                }
            })
        else:
            return Response({
            'main' :  {
                'message' : f'Cart was successfully deleted',
                'error' : False  
                }
            })
        
