from django.urls import path

from .views import add_to_cart_json, remove_from_cart_json, cart_view


app_name = "orders"
urlpatterns = [
    path("add-to-cart/<slug:slug>/", add_to_cart_json, name="add_to_cart"),
    path(
        "remove_from_cart/<slug:slug>/", remove_from_cart_json, name="remove_from_cart"
    ),
    path("cart/", cart_view, name="cart_view"),
]
