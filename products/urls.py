from django.urls import path

from .views import HomeView, ProductListView, ProductDetailView, product_main_image_view


app_name = "products"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "products/<slug:slug>/product_main_image/",
        product_main_image_view,
        name="product_main_image",
    ),
]
