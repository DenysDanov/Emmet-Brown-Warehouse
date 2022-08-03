from django.urls import path
from rest_framework.authtoken import views as drf_views

from . import views

app_name = 'api'
urlpatterns = [
    path('product/', views.ProductApiView.as_view(), name='product'),
    path('product/<int:pk>/', views.ProductApiUpdate.as_view()),
    path('product/detail/<int:pk>/', views.ProductApiDetail.as_view(),name='prod_detail'),
    path('category/', views.CategoryApiView.as_view()),
    path('cart/', views.CartApiView.as_view()),
    path('cart/order/', views.CartApiOrder.as_view()),
    path('users/', views.UserApiView.as_view()),
    path('token/', drf_views.obtain_auth_token),
]