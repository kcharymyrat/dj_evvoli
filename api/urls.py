from django.urls import path

from .views import CategoryListAPIView, ProductListAPIView

app_name = "api"
urlpatterns = [
    path("v1/categories/", CategoryListAPIView.as_view(), name="category_list_api"),
    path("v1/products/", ProductListAPIView.as_view(), name="product_list_api"),
]
