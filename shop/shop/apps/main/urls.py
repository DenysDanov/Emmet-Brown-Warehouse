from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:prod_id>/', views.ProductPage.as_view(), name='cart'),
    path('category/<int:id>/', views.CategoryPage.as_view(), name='cart'),
    path('addtocart/', views.addToCart, name='addtocart'),
    path('cart/order/', views.order, name='order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)