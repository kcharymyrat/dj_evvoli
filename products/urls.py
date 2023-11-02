from django.urls import path

from .views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    product_main_image_view,
    # HTMX
    category_list_view,
    product_elements_list_view,
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

htmxpatterns = [
    path(
        "categories/<slug:category_slug>/",
        category_list_view,
        name="category_list",
    ),
    path(
        "cat/product_list/yo/", product_elements_list_view, name="product_elements_list"
    ),
]


urlpatterns += htmxpatterns
