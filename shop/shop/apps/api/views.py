from django.http import HttpRequest

from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend

from main.cart import Cart
from main.models import Product, Category
from main.service import ReadOnly
from .service import *
from .serializers import CategorySerializer, ProductSerializer, UserSerializer
from .redis_servers import *


class ProductApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id', 'category']
    
    permission_classes = [IsAdminUser|ReadOnly]

class ProductApiUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductApiDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser|ReadOnly]

class CategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CartApiOrder(APIView):
    def post(self, request: HttpRequest):
        Cart(r, id=user_cart_store.get(
           get_user_id_by_token(get_token_from_request(request)) 
        )).order()
        return Response({'success' : True})

class CartApiView(APIView):
    
    permission_classes = [IsAdminUser|ReadOnly]

    def get(self, request):
        cart = Cart(
            id=request.data.get('cart'),
            user=request.user

        ).getproducts()
    
        return Response({
            'id' : request.session.get('cart'),
            'cart' :  cart
            })

    def post(self, request):
        try:
            prod_id = request.POST.get('prod_id')
            quantity = request.POST.get('quantity')
            Cart(
                id=request.data.get('id')
                ).addproduct(
                    prod_id, quantity
                    ).save()

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
            cart = Cart(
                id=request.data.get('cart')
                ).delete()
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
        
class UserApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
