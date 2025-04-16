from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from product.models import Product


class ProductListSerializer(ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', "category_name", "name", "rating", 'is_available', "price", 'sale_price', 'sale', 'views', 'image_list']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None


class ProductDetailSerializer(ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['id', "category_name", "name", "rating", 'is_available',  "price", 'sale_price', 'sale',
                  'code', 'type', 'about', 'information', 'views', 'category', 'image_list']


    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

        # if obj.category:
        #     return obj.category.name
        # else:
        #     return None