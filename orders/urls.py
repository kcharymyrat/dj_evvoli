from django.urls import path

from .views import (
    add_to_cart,
    remove_from_cart,
)


app_name = "orders"
urlpatterns = [
    path("add-to-cart/<slug:slug>/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<slug:slug>/", remove_from_cart, name="remove_from_cart"),
]
