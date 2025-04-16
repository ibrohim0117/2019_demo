from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductListSerializer, ProductDetailSerializer
from .filters import ProductFilter
from product.models import Product


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filterset_class = ProductFilter
    filterset_fields = ['name', ]
    search_fields = ['name', ]
    permission_classes = [IsAuthenticated]




class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=self.kwargs.get("pk"))
        product.update_views()
        serializer = ProductDetailSerializer(product)
        data = {
            'message': 'success',
            'product': serializer.data,
        }
        return Response(data)




