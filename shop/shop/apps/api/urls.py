from django.urls import path

from . import views


urlpatterns = [
    path('product/', views.ProductApiView.as_view()),
    path('product/<int:pk>/', views.ProductApiUpdate.as_view()),
    path('product/detail/<int:pk>/', views.ProductApiDetail.as_view()),
    path('category/', views.CategoryApiView.as_view()),
    path('cart/', views.CartApiView.as_view()),
    path('cart/order/', views.CartApiOrder.as_view()),
]