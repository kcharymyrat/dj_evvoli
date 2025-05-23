import logging
import time

from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderForm

from products.models import Product

logger = logging.getLogger(__name__)  # For general application logging (console)
django_logger = logging.getLogger("django")  # For DJANGO-specific logging
api_logger = logging.getLogger("api")  # For API-specific logging


@require_POST
def add_to_cart_json(request, slug):
    # for key in list(request.session.keys()):
    #     if key.startswith("cart"):
    #         del request.session[key]
    #     request.session.modified = True

    try:
        product = get_object_or_404(Product, slug=slug)

        cart_id = request.session.get("cart_id")
        if cart_id:
            # Prefetch the related CartItem instances
            cart = get_object_or_404(
                Cart.objects.prefetch_related("cart_items__product"), id=cart_id
            )
        else:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id

        cart_item_as_lst = [
            item for item in cart.cart_items.all() if item.product == product
        ]
        if cart_item_as_lst:
            cart_item = cart_item_as_lst[0]
            if cart_item.quantity < 100:
                cart_item.quantity += 1
                cart_item.save()

        else:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()

        cart.refresh_from_db()

        request.session["cart_qty"] = cart.total_quantity
        request.session.modified = True

        cart_qty = request.session["cart_qty"]
        product_qty = cart_item.quantity

        return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})

    except Exception:
        return JsonResponse({"error": "No such product"}, status=404)


@require_POST
def remove_from_cart_json(request, *args, **kwargs):
    # If there's no cart in the session, return an error
    print("kwargs =", kwargs)
    if "cart_id" not in request.session:
        return JsonResponse({"error": "No cart found"}, status=404)

    try:
        # Get the product and cart from the database
        slug = kwargs["slug"]  # slug is product slug
        product = get_object_or_404(Product, slug=slug)
        cart_id = request.session["cart_id"]
        cart = get_object_or_404(
            Cart.objects.prefetch_related("cart_items__product"), id=cart_id
        )

        # Get the cart item for the product
        cart_item_as_lst = [
            item for item in cart.cart_items.all() if item.product == product
        ]
        cart_item = cart_item_as_lst[0]

        with transaction.atomic():
            # If the cart item exists and its quantity is greater than 0, decrease the quantity
            if cart_item.quantity > 0:
                cart_item.quantity -= 1
                # If the quantity is now 0, delete the cart item
                if cart_item.quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.save()

        cart.refresh_from_db()

        # Calculate the total quantity of items in the cart and the quantity of the product
        cart_qty = cart.total_quantity
        product_qty = cart_item.quantity if cart_item.pk else 0

        # Save the total quantity in the session
        request.session["cart_qty"] = cart_qty

        return JsonResponse({"cartQty": cart_qty, "productQty": product_qty})

    except Exception:
        return JsonResponse({"error": "Something went wrong"}, status=500)


def cart_view(request, *args, **kwargs):
    if "cart_id" not in request.session:
        if request.htmx:
            return render(request, "orders/partials/no_products_in_cart_partial.html")
        return render(request, "orders/no_products_in_cart.html")

    cart = (
        Cart.objects.filter(id=request.session["cart_id"])
        .prefetch_related("cart_items__product__category")
        .first()
    )

    if not cart:
        for key in list(request.session.keys()):
            if key.startswith("cart"):
                del request.session[key]
            request.session.modified = True

        if request.htmx:
            return render(request, "orders/partials/no_products_in_cart_partial.html")
        return render(request, "orders/no_products_in_cart.html")

    if not cart.cart_items.all():
        if request.htmx:
            return render(request, "orders/partials/no_products_in_cart_partial.html")
        return render(request, "orders/no_products_in_cart.html")
    context = {"cart": cart}

    if request.htmx:
        return render(request, "orders/partials/cart_partial.html", context)
    return render(request, "orders/cart.html", context)


def cart_checkout_details(request, *args, **kwargs):
    if "cart_id" not in request.session:
        return render(request, "orders/partials/no_products_in_cart_partial.html")
    cart = (
        Cart.objects.filter(id=request.session["cart_id"])
        .prefetch_related("cart_items__product__category")
        .first()
    )
    context = {"cart": cart}
    print(context)
    return render(request, "orders/partials/cart_checkout_details.html", context)


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm

    def dispatch(self, request, *args, **kwargs):
        self.cart = None
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            self.cart_id = cart_id
            self.cart = (
                Cart.objects.filter(id=cart_id)
                .prefetch_related("cart_items__product__category")
                .first()
            )

            if not self.cart:
                # Clear session entries starting with "cart"
                cart_keys = [
                    key for key in request.session.keys() if key.startswith("cart")
                ]
                for key in cart_keys:
                    del request.session[key]

                # Create a new cart and save its ID in the session
                new_cart = Cart.objects.create()
                request.session["cart_id"] = new_cart.id
                self.request.session.modified = True

                # Deliver the message and redirect
                messages.info(request, _("A new cart has been created for you."))
                return redirect("products:home")

            context = {"self.cart": self.cart}
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            order = form.save(commit=False)
            if self.cart:
                form.instance.cart = self.cart
                order.cart = self.cart
                order.save()
                for cart_item in self.cart.cart_items.all():
                    OrderItem.objects.create(
                        order=order,
                        product_title=cart_item.product.title,
                        product_model=cart_item.product.model,
                        product_price=cart_item.product.sale_price,
                        quantity=cart_item.quantity,
                    )
                order.update_total_price()
                order.save()

        return super().form_valid(form)

    def get_success_url(self):
        for key in list(self.request.session.keys()):
            if key.startswith("cart"):
                del self.request.session[key]
        self.request.session.modified = True
        return reverse("orders:order_success", kwargs={"order_id": self.object.id})

    def get_template_names(self):
        if self.request.htmx:
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
        return context


class OrderSuccessDetailView(TemplateView):
    model = Order

    def get_template_names(self):
        if self.request.htmx:
            return "orders/partials/order_success_partial.html"
        return "orders/order_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs["order_id"]
        order = get_object_or_404(Order, id=order_id)
        context["order"] = order
        return context
