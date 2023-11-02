from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.sessions.models import Session

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from uuid import UUID

from .models import Category, Product, ProductImage

from orders.models import Cart, CartItem, Order


def search(request):
    query = request.GET.get("q")
    if query is not None and query != "":
        products = Product.objects.filter(
            Q(title__icontains=query)
            | Q(title_en__icontains=query)
            | Q(title_ru__icontains=query)
        ).distinct()
    else:
        products = Product.objects.all()
    return render(
        request, "products/search_results.html", context={"products": products}
    )


class HomeView(ListView):
    model = Category
    paginate_by = 2
    context_object_name = "categories"

    def get_template_names(self):
        if self.request.htmx:
            return "includes/category_list_elements.html"
        return "index.html"


def product_list_element(request, *args, **kwargs):
    category_slug = kwargs.get("category_slug")
    page_number = request.GET.get("page")
    print(f"page_number = {page_number}")


def category_list_view(request, *args, **kwargs):
    category_slug = kwargs.get("category_slug")
    page_number = request.GET.get("page", 1)
    print(f"page_number = {page_number}")
    print("request.htmx", request.htmx)
    print("request.htmx.target =", request.htmx.target)
    print("request.htmx.trigger =", request.htmx.trigger)
    print("request.htmx.boosted =", request.htmx.boosted)

    category = Category.objects.filter(slug=category_slug).first()
    category_products = category.products.all()
    paginator = Paginator(category_products, 2)

    product_types = set(category.products.values_list("type", flat=True).distinct())
    print("product_types =", product_types)

    context = {"products": paginator.get_page(page_number)}
    context["category_slug"] = category_slug
    context["types"] = product_types
    if request.htmx:
        print("htmx")
        print("request.htmx", request.htmx)
        print("request.htmx.target =", request.htmx.target)
        print("request.htmx.trigger =", request.htmx.trigger)
        print("request.htmx.boosted =", request.htmx.boosted)

        return render(
            request, "categories/partials/categories_partial_htmx.html", context
        )
    print("non htmx")
    return render(request, "categories/categories_htmx.html", context)


products_global = []


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = "products"

    def get_template_names(self):
        category_slug = self.kwargs.get("category_slug")
        if self.request.htmx:
            return "products/components/product_list_elements.html"
        products_global = (
            Category.objects.filter(slug=category_slug).first().products.all()
        )
        return "products/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get("category_slug")
        context["category_slug"] = category_slug

        # send product types
        types = set(
            Category.objects.filter(slug=category_slug)
            .first()
            .products.values_list("type", flat=True)
            .distinct()
        )
        context["types"] = types
        return context

    def get_queryset(self):
        global products_global
        request = self.request

        category_slug = self.kwargs.get("category_slug")
        category = Category.objects.filter(slug=category_slug).first()

        if not products_global:
            products_global = category.products.all()

        if products_global.first():
            product_category_slug = products_global.first().category.slug
            if product_category_slug != category_slug:
                products_global = category.products.all()

        if request.htmx.trigger == "product_type_form":
            product_type = request.GET.get("product_type")
            products_global = category.products.filter(type=product_type)

            # Check if all product types was chose
            if product_type == "all":
                products_global = category.products.all()

            # Check for on sale - maybe will have to change it to context processor later???
            on_sale = request.GET.get("on_sale")
            if on_sale:
                products_global = products_global.filter(on_sale=True)

            # Check the price range
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            if min_price and max_price:
                products_global = products_global.filter(
                    price__gt=min_price, price__lt=max_price
                )
            elif min_price:
                products_global = products_global.filter(price__gt=min_price)
            elif max_price:
                products_global = products_global.filter(price__lt=max_price)
            return products_global
        elif request.htmx.trigger == "last_product_page":
            return products_global
        return products_global


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail_async_js.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_qty_in_cart = 0
        cart_id = self.request.session.get("cart_id", None)

        if not cart_id:
            context["product_qty_in_cart"] = product_qty_in_cart
            return context

        cart = get_object_or_404(Cart, id=cart_id)
        if cart:
            for cart_item in cart.cart_items.all():
                print(
                    f"cart_item = {cart_item}, {cart_item.product} {context['object']} {cart_item.quantity}"
                )
                if context["object"] == cart_item.product and cart_item.quantity > 0:
                    product_qty_in_cart = cart_item.quantity
        context["product_qty_in_cart"] = product_qty_in_cart
        return context


def product_main_image_view(request, *args, **kwargs):
    product_id = UUID(request.GET.get("product_id"))
    product = Product.objects.filter(id=product_id).first()
    image_id = request.GET.get("image_id")
    if image_id:
        image_id = UUID(request.GET.get("image_id"))
        image = ProductImage.objects.filter(id=image_id).first()
        context = {"product": product, "image": image}
    else:
        image = "main"
        context = {"product": product}
    return render(request, "products/components/product_main_image.html", context)
