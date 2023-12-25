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
    CartItemProductSerializer,
    CartItemSerializer,
    CartSerializer,
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
        return Product.objects.filter(category__id=category_id)


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class EmptyCategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(name="Yoyo")
    serializer_class = CategorySerializer


class CartDetailAPIView(RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class AddProductToCartAPIView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {"message": "Product ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = get_object_or_404(Product, pk=product_id)

        cart, created = Cart.objects.get_or_create(is_ordered=False)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += int(quantity)
        cart_item.save()
        cart.update_total_price()

        return Response(
            {"message": "Product added to cart successfully"}, status=status.HTTP_200_OK
        )


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
        products = Product.objects.filter(
            Q(title__icontains=query)
            | Q(title_en__icontains=query)
            | Q(title_ru__icontains=query)
            | Q(model__icontains=query)
            | Q(category__in=categories)
            | Q(type__icontains=query)
            | Q(type_en__icontains=query)
            | Q(type_ru__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()

    return products
