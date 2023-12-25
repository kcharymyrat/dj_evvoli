from django.urls import path

from .views import (
    CategoryListAPIView,
    CategoryProductListAPIView,
    ProductDetailAPIView,
    ProductSearchListAPIView,
    OrderCreateAPIView,
)

app_name = "api"
urlpatterns = [
    path("v1/categories/", CategoryListAPIView.as_view(), name="category_list_api"),
    path(
        "v1/categories/<uuid:category_id>/products/",
        CategoryProductListAPIView.as_view(),
        name="product_list_api",
    ),
    path(
        "v1/products/<uuid:pk>/",
        ProductDetailAPIView.as_view(),
        name="product_detail_api",
    ),
    path(
        "v1/search/",
        ProductSearchListAPIView.as_view(),
        name="search_api",
    ),
    path("v1/create-order/", OrderCreateAPIView.as_view(), name="create-order"),
]
