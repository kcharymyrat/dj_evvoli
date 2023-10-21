from django.urls import path

from .views import HomeTemplateView, ProductListView


app_name = "products"
urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("products/", ProductListView.as_view(), name="product_list"),
]
