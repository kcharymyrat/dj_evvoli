from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST

from .models import Cart, CartItem, Order
from products.models import Category, Product


@require_POST
def add_to_cart_json(request, *args, **kwargs):
    slug = kwargs["slug"]
    product = get_object_or_404(Product, slug=slug)

    if "cart_id" not in request.session:
        cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
    else:
        cart = Cart.objects.get(id=request.session["cart_id"])

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)

    cart_item.save()
    cart.update_total_price()

    cart_qty = 0
    product_qty = 0
    for item in cart.cart_items.all():
        cart_qty += item.quantity
        if product == item.product and item.quantity > 0:
            product_qty = cart_item.quantity
    request.session["cart_qty"] = cart_qty
    request.session.save()
    # print({"cart_qty": cart_qty, "product_qty": product_qty})

    return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})


@require_POST
def remove_from_cart_json(request, *args, **kwargs):
    slug = kwargs["slug"]
    product = get_object_or_404(Product, slug=slug)

    if "cart_id" not in request.session:
        return JsonResponse({"error": "No cart found"}, status=404)

    cart = Cart.objects.get(id=request.session["cart_id"])

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        return JsonResponse({"error": "No cart item found"}, status=404)

    cart.update_total_price()

    cart_qty = 0
    product_qty = 0
    for item in cart.cart_items.all():
        cart_qty += item.quantity
        if product == item.product and item.quantity > 0:
            product_qty = cart_item.quantity
    request.session["cart_qty"] = cart_qty
    request.session.save()
    # print({"cart_qty": cart_qty, "product_qty": product_qty})

    return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})


def cart_view(request, *args, **kwargs):
    if "cart_id" not in request.session:
        return Http404()  # Better implement you don't have a cart yet
    cart = get_object_or_404(Cart, id=request.session["cart_id"])
    print(f"cart = {cart}")
    print([items for items in cart.cart_items.all()])
    context = {"cart": cart}
    print(context)
    return render(request, "orders/cart.html", context)
