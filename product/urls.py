from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
]