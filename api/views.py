from rest_framework.generics import ListAPIView

from .serializers import CategorySerializer, ProductSerializer

from products.models import Category, Product


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
