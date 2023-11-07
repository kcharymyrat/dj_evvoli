from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponse
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from .models import Cart, CartItem, Order
from .forms import OrderForm

from products.models import Category, Product


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        print(
            "session =", [{key: value} for key, value in self.request.session.items()]
        )
        self.cart = None
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            self.cart_id = cart_id
            self.cart = get_object_or_404(Cart, id=cart_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user:
            form.instance.user = self.request.user
        if self.cart:
            form.instance.cart = self.cart
        return super().form_valid(form)

    def get_success_url(self):
        for key in list(self.request.session.keys()):
            if key.startswith("cart"):
                del self.request.session[key]
        print(
            "session =", [{key: value} for key, value in self.request.session.items()]
        )
        self.request.session.modified = True
        return reverse("products:home")

    def get_template_names(self):
        if self.request.htmx:
            print("\n\norder: self.request.htmx:")
            if self.cart and self.cart.total_quantity > 0:
                return "orders/partials/order_form_partial.html"
            return "orders/partials/order_not_allowed_partial.html"
        if self.cart and self.cart.total_quantity > 0:
            return "orders/order_form.html"
        return "orders/order_not_allowed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.cart:
            context["cart"] = self.cart
        print(context)
        return context


@require_POST
def add_to_cart_json(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Exception:
        return JsonResponse({"error": "No such product"}, status=404)

    with transaction.atomic():
        if "cart_id" not in request.session:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
        else:
            cart = Cart.objects.get(id=request.session["cart_id"])

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart.refresh_from_db()

        request.session["cart_qty"] = cart.total_quantity
        request.session.save()

    cart_qty = request.session["cart_qty"]
    product_qty = cart_item.quantity

    return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})


@require_POST
def remove_from_cart_json(request, *args, **kwargs):
    # If there's no cart in the session, return an error
    if "cart_id" not in request.session:
        return JsonResponse({"error": "No cart found"}, status=404)

    try:
        # Get the product and cart from the database
        slug = kwargs["slug"]  # slug is product slug
        product = get_object_or_404(Product, slug=slug)
        cart = get_object_or_404(Cart, id=request.session["cart_id"])

        # Get the cart item for the product
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)

        with transaction.atomic():
            # If the cart item exists and its quantity is greater than 0, decrease the quantity
            print("cart_item.quantity =", cart_item.quantity)
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                print("cart_item.quantity =", cart_item.quantity)

                # If the quantity is now 0, delete the cart item
                if cart_item.quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.save()

            # Calculate the total quantity of items in the cart and the quantity of the product
            cart_qty = sum(item.quantity for item in cart.cart_items.all())
            product_qty = cart_item.quantity if cart_item.pk else 0

            # Save the total quantity in the session
            request.session["cart_qty"] = cart_qty

        return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})

    except Exception:
        return JsonResponse({"error": "Something went wrong"}, status=500)


def cart_view(request, *args, **kwargs):
    print("\n\n\ncart_view(request, *args, **kwargs)")
    for k, v in request.session.items():
        print(f"{k}: {v}")
    # del request.session["cart_id"]
    # del request.session["cart_qty"]
    request.session.save()
    if "cart_id" not in request.session:
        if request.htmx:
            print('"cart_id" not in request.session: - htmx')
            return render(request, "orders/partials/no_products_in_cart_partial.html")
        print('"cart_id" not in request.session: - NOT htmx')
        return render(request, "orders/no_products_in_cart.html")
    cart = get_object_or_404(Cart, id=request.session["cart_id"])
    print(f"cart = {cart}")
    print([items for items in cart.cart_items.all()])
    context = {"cart": cart}
    print(context)
    if request.htmx:
        print("htmx cart_view(request, *args, **kwargs)")
        return render(request, "orders/partials/cart_partial.html", context)
    print("not htmx cart_view(request, *args, **kwargs)")
    return render(request, "orders/cart.html", context)


def cart_checkout_details(request, *args, **kwargs):
    print("\n\n\ncart_checkout_details(request, *args, **kwargs)")
    for k, v in request.session.items():
        print(f"{k}: {v}")
    # del request.session["cart_id"]
    # del request.session["cart_qty"]
    request.session.save()
    if "cart_id" not in request.session:
        return render(request, "orders/partials/no_products_in_cart_partial.html")
    cart = get_object_or_404(Cart, id=request.session["cart_id"])
    print(f"cart = {cart}")
    print([items for items in cart.cart_items.all()])
    context = {"cart": cart}
    print(context)
    return render(request, "orders/partials/cart_checkout_details.html", context)
