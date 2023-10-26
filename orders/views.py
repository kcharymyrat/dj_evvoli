from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.sessions.models import Session

from .models import Cart, CartItem, Order
from products.models import Category, Product


def add_to_cart(request, *args, **kwargs):
    slug = kwargs["slug"]
    product = get_object_or_404(Product, slug=slug)
    print(f"\nslug={slug}, product= {product}")

    for k, v in request.session.items():
        print(f"{k}: {v}")

    # del request.session["cart_id"]  # TO DELETE IT ONCE MORE
    # request.session.save()

    # Check if the cart is in the session
    if "cart_id" in request.session:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
    else:
        # If not, create a new cart and save its id in the session
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id

    # Check if the cart item already exists
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": 1}
    )

    # If the cart item already exists, increment the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    cart.save()
    print(
        f'request.session["cart_id"] = {request.session["cart_id"]}, {type(request.session["cart_id"])}'
    )
    print(f"cart_item = {cart_item}")
    print(f"cart.products = {cart.products.all()}")
    # del request.session["cart_id"]  # TO DELETE IT ONCE MORE

    quantity = 0
    for cart_item in cart.cart_items.all():
        print(f"cart_item = {cart_item}, {cart_item.product}")
        quantity += cart_item.quantity
    cart.update_total_price()
    context = {"quantity": quantity}
    print(f"context = {context}")

    request.session["cart_qty"] = quantity
    print(f"request.session = {request.session}")
    request.session.save()
    return render(request, "products/components/cart_qty.html", context)


def remove_from_cart(request, *args, **kwargs):
    quantity = 0
    slug = kwargs["slug"]
    product = get_object_or_404(Product, slug=slug)
    print(f"\nslug={slug}, product= {product}")

    for k, v in request.session.items():
        print(f"{k}: {v}")

    # del request.session["cart"]  # TO DELETE IT ONCE MORE

    # Check if the cart is in the session
    if "cart_id" in request.session:
        cart_id = request.session["cart_id"]
        cart = Cart.objects.get(id=cart_id)
        print(f"cart = {cart}")
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if product != cart_item.product:
            return Http404("requested page does not work!")
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            quantity = cart_item.quantity
            cart_item.save()
            cart.update_total_price()
            cart.save()
            print(f"cart_item = {cart_item}")
            print(f"cart = {cart}")
        else:
            cart_item.delete()
            cart.update_total_price()
            cart.save()
            print(f"cart = {cart}")

    print(f"cart.products = {cart.products.all()}")
    # del request.session["cart_id"]  # TO DELETE IT ONCE MORE

    context = {"quantity": quantity}
    print(f"context = {context}")

    request.session["cart_qty"] = quantity
    print(f"request.session = {request.session}")
    request.session.save()

    for k, v in request.session.items():
        print(f"{k}: {v}")

    return render(request, "products/components/cart_qty.html", context)


# def createCartItem


def view_cart(request):
    cart = request.session.get("cart", {})
