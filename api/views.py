from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
    OrderCreateSerializer,
)

from products.models import Category, Product
from orders.models import CartItem, Cart, Order


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the products for
        the category as determined by the category portion of the URL.
        """
        category_id = self.kwargs["category_id"]
        return Product.objects.filter(category__id=category_id).filter(in_stock=True)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all().filter(in_stock=True)
    serializer_class = ProductDetailSerializer


class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                {"message": "Order created successfully", "order_id": order.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductSearchListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        This view should return a list of all the products for
        the category as determined by the category portion of the URL.
        """
        query = self.request.GET.get("q", "").strip()
        return get_filetered_products(query)


def get_filetered_products(query):
    if query:
        categories = Category.objects.filter(
            Q(name__icontains=query)
            | Q(name_en__icontains=query)
            | Q(name_ru__icontains=query)
        )
        products = (
            Product.objects.filter(
                Q(model__icontains=query)
                | Q(category__in=categories)
                | Q(type__icontains=query)
                | Q(type_en__icontains=query)
                | Q(type_ru__icontains=query)
            )
            .filter(in_stock=True)
            .distinct()
        )
    else:
        products = Product.objects.none()

    return products
