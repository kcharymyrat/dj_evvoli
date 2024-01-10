from django.urls import path

from .views import (
    category_list_view,
    HomeListView,
    ProductDetailView,
    product_main_image_view,
    search_view,
    AboutView,
    ProductVideoView,
)


app_name = "products"
urlpatterns = []

htmxpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("search/", search_view, name="search"),
    path("about/", AboutView.as_view(), name="about"),
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
        "products/<slug:category_slug>/<slug:slug>/product-main-image/",
        product_main_image_view,
        name="product_main_image",
    ),
    path(
        "product-video/<slug:slug>/",
        ProductVideoView.as_view(),
        name="product_video",
    ),
]


urlpatterns += htmxpatterns
