from django.urls import path

from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    product_main_image_view,
)


app_name = "products"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "products/<slug:category_slug>/",
        ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "products/<slug:category_slug>/<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/<slug:category_slug>/<slug:slug>/product_main_image/",
        product_main_image_view,
        name="product_main_image",
    ),
]
