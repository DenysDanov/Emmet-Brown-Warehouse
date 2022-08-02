from datetime import timedelta
from django.db import models
from django.views.generic import ListView, DetailView
from django.http import HttpRequest
from django.shortcuts import redirect, render

from .service import allowed_methods
from .models import Product, Category
from .cart import Cart
from api.views import r, user_cart_store
import api.views as API


# additional context
menu = [
    {'text' : 'Кошик', 'url' : 'http://localhost/cart'},
    {'text' : 'Головна', 'url' : 'http://localhost/'},
    ]

footer = []

class MainView(ListView):
    model = Product
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = 'Emmet Brown Warehouse'
        context['menu'] = menu
        context['stylename'] = 'index'
        context['footer'] = footer
        return context

class ProductPage(DetailView):
    model = Product
    pk_url_kwarg = 'prod_id'
    template_name = 'main/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Emmet Brown Warehouse'
        context['menu'] = menu
        context['stylename'] = 'product'
        context['footer'] = footer
        return context

class CategoryPage(ListView):
    model = Category
    pk_url_kwarg = 'id'
    template_name = 'main/category.html'

    def get_queryset(self) -> models.query.QuerySet:
        return Product.objects.filter(category=Category.objects.get(pk=self.kwargs.get('id')))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Emmet Brown Warehouse'
        context['menu'] = menu
        context['stylename'] = 'category'
        context['footer'] = footer
        return context

def cart(request : HttpRequest):
    return render(request, 'main/cart.html', {
        'cart': Cart(r, user_cart_store, request).getproducts(),
        'menu': menu,
        'title': 'Cart',
        'stylename': 'cart',
        'footer': footer,
        
        })

@allowed_methods('POST')
def addToCart(request : HttpRequest):
    try:
        prod_id = request.POST.get('prod_id')
        quantity = request.POST.get('quantity')
        Cart(r, user_cart_store, request).addproduct(prod_id, quantity).save()
        return redirect('/')
    except Exception as e:
        pass


@allowed_methods('POST')
def order(request : HttpRequest):
    Cart(r, user_cart_store, request).order()
    return redirect('..')