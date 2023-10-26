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
            print("HTMX requst triggered")
            return "includes/category_list_elements.html"
        return "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


products_global = []


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = "products"

    def get_template_names(self):
        category_slug = self.kwargs.get("category_slug")
        print(f"\nget_template category_slug={category_slug}")
        if self.request.htmx:
            return "products/components/product_list_elements.html"
        products_global = (
            Category.objects.filter(slug=category_slug).first().products.all()
        )
        return "products/products.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get("category_slug")
        print(":::::::::::::::::::::::::::::::::::::::")
        print("context =", context)
        print(f"\nget_queryset category_slug={category_slug}")
        context["category_slug"] = category_slug

        # send product types
        types = set(
            Category.objects.filter(slug=category_slug)
            .first()
            .products.values_list("type", flat=True)
            .distinct()
        )
        print(f"types = {types}")
        context["types"] = types
        print(context)
        return context

    def get_queryset(self):
        global products_global

        category_slug = self.kwargs.get("category_slug")
        print(f"\nget_queryset category_slug={category_slug}")
        category = Category.objects.filter(slug=category_slug).first()

        print(f"products_global = {products_global}")
        if not products_global:
            products_global = category.products.all()

        print(f"products_global.first() = {products_global.first()}")

        if products_global.first():
            product_category_slug = products_global.first().category.slug
            print(f"product_category_slug = {product_category_slug}")
            if product_category_slug != category_slug:
                products_global = category.products.all()

        request = self.request

        if request.htmx.trigger == "product_type_form":
            print("in request.htmx.trigger == product_type_form")
            product_type = request.GET.get("product_type")
            print(f"product_type = {product_type}")
            products_global = category.products.filter(type=product_type)
            print(f"products_global = {products_global}")
            print(f"product_type = {product_type}, {type(product_type)}")

            # Check if all product types was chose
            if product_type == "all":
                print('in product_type == "all"')
                products_global = category.products.all()

            # Check for on sale - maybe will have to change it to context processor later???
            on_sale = request.GET.get("on_sale")
            print(f"on_sale = {on_sale}")
            if on_sale:
                products_global = products_global.filter(on_sale=True)

            # Check the price range
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            print(f"min_price = {min_price}")
            print(f"max_price = {max_price}")
            if min_price and max_price:
                products_global = products_global.filter(
                    price__gt=min_price, price__lt=max_price
                )
            elif min_price:
                products_global = products_global.filter(price__gt=min_price)
            elif max_price:
                products_global = products_global.filter(price__lt=max_price)

            print(f"products_global = {products_global}")
            return products_global
        elif request.htmx.trigger == "last_product_page":
            print('in request.htmx.trigger == "last_product_page"')
            print(f"products_global = {products_global}")
            return products_global
        return products_global


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail_xander.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # del self.request.session["cart_qty"]
        # self.request.session.save()

        for k, v in self.request.session.items():
            print(f"{k}: {v}")

        product_qty_in_cart = 0
        cart_id = self.request.session.get("cart_id", None)

        if not cart_id:
            context["product_qty_in_cart"] = product_qty_in_cart
            print(f"context = {context}")
            return context

        cart = get_object_or_404(Cart, id=cart_id)
        print(f"cart = {cart}")
        if cart:
            for cart_item in cart.cart_items.all():
                print(
                    f"cart_item = {cart_item}, {cart_item.product} {context['object']} {cart_item.quantity}"
                )
                if context["object"] == cart_item.product and cart_item.quantity > 0:
                    product_qty_in_cart = cart_item.quantity
        print(f"product_qty_in_cart = {product_qty_in_cart}")
        context["product_qty_in_cart"] = product_qty_in_cart
        print(f"context = {context}")
        return context


def product_main_image_view(request, *args, **kwargs):
    print(f"request.GET = {request.GET}")
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
    print(f"product_id = {product_id}, image_id = {image_id}")

    print(context)
    return render(request, "products/components/product_main_image.html", context)
