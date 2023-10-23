from django.urls import path

from .views import ProductListView, HomeView


app_name = "products"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
]
