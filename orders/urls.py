from django.urls import path

from .views import (
    add_to_cart_json,
    remove_from_cart_json,
    cart_view,
    cart_checkout_details,
)


app_name = "orders"
urlpatterns = [
    path("add-to-cart/<slug:slug>/", add_to_cart_json, name="add_to_cart"),
    path(
        "remove-from-cart/<slug:slug>/", remove_from_cart_json, name="remove_from_cart"
    ),
    path("cart/", cart_view, name="cart_view"),
    path(
        "cart/cart-checkout-details/",
        cart_checkout_details,
        name="cart_checkout_details",
    ),
]
