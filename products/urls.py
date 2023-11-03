from django.urls import path

from .views import (
    OldHomeView,
    OldProductListView,
    OldProductDetailView,
    product_main_image_view,
    # HTMX
    category_list_view,
    HomeListView,
    ProductDetailView,
)


app_name = "products"
urlpatterns = [
    path("home/", OldHomeView.as_view(), name="old_home"),
    path(
        "products/<slug:category_slug>/",
        OldProductListView.as_view(),
        name="product_list",
    ),
]

htmxpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path(
        "categories/<slug:category_slug>/",
        category_list_view,
        name="category_list",
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


urlpatterns += htmxpatterns
