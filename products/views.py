import logging

from uuid import UUID

from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language
from django.views.generic import ListView, DetailView, TemplateView

from .models import Category, Product
from orders.models import Cart

logger = logging.getLogger(__name__)  # For general application logging (console)
django_logger = logging.getLogger("django")  # For DJANGO-specific logging
api_logger = logging.getLogger("api")  # For API-specific logging


class HomeListView(ListView):
    model = Category
    paginate_by = 2
    context_object_name = "cats"

    def get_template_names(self):
        if self.request.htmx:
            if self.request.htmx.target == "main-body":
                return "index_partial.html"
            else:
                return "includes/category_list_elements.html"
        return "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def search_view(request):
    query = request.GET.get("q", "").strip()
    if request.method == "POST":
        query = request.POST.get("q", "").strip()
    page_number = request.GET.get("page") or 1

    if query:
        categories = Category.objects.filter(
            Q(name__icontains=query)
            | Q(name_en__icontains=query)
            | Q(name_ru__icontains=query)
        )
        products = (
            Product.objects.filter(
                Q(model__icontains=query)
                | Q(category__in=categories)
                | Q(type__icontains=query)
                | Q(type_en__icontains=query)
                | Q(type_ru__icontains=query)
            )
            .filter(in_stock=True)
            .distinct()
            .prefetch_related("category")
        )
    else:
        products = Product.objects.filter(in_stock=True).prefetch_related("category")

    paginator = Paginator(products, 3)
    page_obj = paginator.get_page(page_number)

    if request.htmx.target == "product_search_elements":
        return render(
            request,
            "categories/partials/product_search_single.html",
            context={"products": page_obj, "query": query},
        )

    return render(
        request,
        "categories/partials/products_search.html",
        context={"products": page_obj, "query": query},
    )


class AboutView(TemplateView):
    def get_template_names(self):
        if self.request.htmx:
            return "about_partial.html"
        return "about.html"


def category_list_view(request, *args, **kwargs):
    if request.htmx:
        current_language = get_language()

        category_slug = kwargs.get("category_slug")
        page_number = request.GET.get("page") or 1

        category = (
            Category.objects.filter(slug=category_slug)
            .prefetch_related("products")
            .first()
        )
        category_products = category.products.all().filter(in_stock=True)
        paginator = Paginator(category_products, 2)
        page_obj = paginator.get_page(page_number)

        if current_language == "en":
            product_types = set([product.type_en for product in category_products])
        elif current_language == "ru":
            product_types = set([product.type_ru for product in category_products])
        else:
            product_types = set([product.type for product in category_products])

        context = {
            "products": page_obj,
            "category_slug": category_slug,
            "types": product_types,
            "page_obj": page_obj,
        }

        if request.htmx.target == "main-body":
            if request.session.get("filter_dict"):
                del request.session["filter_dict"]
            return render(
                request, "categories/partials/categories_partial.html", context
            )

        if request.htmx.trigger == "last_product_page":
            filter_dict = request.session.get("filter_dict")

            # If filter_dict exist
            if filter_dict:
                products = category_products
                product_type = filter_dict.get("product_type")

                # Check if product_type exist:
                if product_type and product_type != "all":
                    if current_language == "en":
                        products = category.products.filter(
                            type_en=product_type
                        ).filter(in_stock=True)
                    elif current_language == "ru":
                        products = category.products.filter(
                            type_ru=product_type
                        ).filter(in_stock=True)
                    else:
                        products = category.products.filter(type=product_type).filter(
                            in_stock=True
                        )

                # Check if all product types was chose
                if product_type == "all":
                    products = category.products.all().filter(in_stock=True)

                # Check for on sale - maybe will have to change it to context processor later???
                on_sale = filter_dict.get("on_sale")
                if on_sale:
                    products = products.filter(on_sale=True)

                # Check the price range
                min_price = filter_dict.get("min_price")
                max_price = filter_dict.get("max_price")
                if min_price and max_price:
                    products = products.filter(price__gt=min_price, price__lt=max_price)
                elif min_price:
                    products = products.filter(price__gt=min_price)
                elif max_price:
                    products = products.filter(price__lt=max_price)

                paginator = Paginator(products, 2)
                page_obj = paginator.get_page(page_number)

                context["products"] = page_obj
                context["page_obj"] = page_obj

            return render(
                request, "categories/partials/product_list_elements.html", context
            )

        elif request.htmx.trigger == "product_type_form":
            page_number = request.GET.get("page") or 1
            product_type = request.GET.get("product_type")
            print("product_type =", product_type)

            # Check if product_type exist:
            if product_type and product_type != "all":
                if current_language == "en":
                    products = category.products.filter(type_en=product_type).filter(
                        in_stock=True
                    )
                elif current_language == "ru":
                    products = category.products.filter(type_ru=product_type).filter(
                        in_stock=True
                    )
                else:
                    products = category.products.filter(type=product_type).filter(
                        in_stock=True
                    )

            # Check if all product types was chose
            if product_type == "all":
                products = category.products.all().filter(in_stock=True)

            # Check for on sale - maybe will have to change it to context processor later???
            on_sale = request.GET.get("on_sale")
            if on_sale:
                products = products.filter(on_sale=True).filter(in_stock=True)

            # Check the price range
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            if min_price and max_price:
                products = products.filter(
                    price__gt=min_price, price__lt=max_price
                ).filter(in_stock=True)
            elif min_price:
                products = products.filter(price__gt=min_price).filter(in_stock=True)
            elif max_price:
                products = products.filter(price__lt=max_price).filter(in_stock=True)

            paginator = Paginator(products, 2)
            page_obj = paginator.get_page(page_number)

            context["products"] = page_obj
            context["page_obj"] = page_obj

            # save product_type into session
            filter_dict = {}
            for key, value in request.GET.items():
                filter_dict[key] = value
            request.session["filter_dict"] = filter_dict
            request.session.modified = True

            return render(
                request, "categories/partials/product_list_elements.html", context
            )

    # Delete filter_dict if in session
    if request.session.get("filter_dict"):
        del request.session["filter_dict"]
    return all_product_elements_list_view(request, kwargs)


def all_product_elements_list_view(request, kwargs):
    current_language = get_language()

    category_slug = kwargs.get("category_slug")
    page_number = request.GET.get("page") or 1

    category = (
        Category.objects.filter(slug=category_slug).prefetch_related("products").first()
    )
    category_products = category.products.all().filter(
        in_stock=True
    )  # This won't hit the database again because of prefetch_related
    paginator = Paginator(category_products, 2)
    page_obj = paginator.get_page(page_number)

    if current_language == "en":
        product_types = set([product.type_en for product in category_products])
    elif current_language == "ru":
        product_types = set([product.type_ru for product in category_products])
    else:
        product_types = set([product.type for product in category_products])

    context = {
        "products": page_obj,
        "category_slug": category_slug,
        "types": product_types,
        "page_obj": page_obj,
    }

    return render(request, "categories/categories.html", context)


class ProductDetailView(DetailView):
    model = Product

    def get_template_names(self):
        if self.request.htmx:
            return "categories/partials/product_detail_partial.html"
        return "categories/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_qty_in_cart = 0
        cart_id = self.request.session.get("cart_id", None)

        if not cart_id:
            context["product_qty_in_cart"] = product_qty_in_cart
            return context

        # cart = get_object_or_404(Cart, id=cart_id)
        cart = (
            Cart.objects.filter(id=cart_id)
            .prefetch_related("cart_items__product")
            .first()
        )
        if cart:
            for cart_item in cart.cart_items.all():
                if context["object"] == cart_item.product and cart_item.quantity > 0:
                    product_qty_in_cart = cart_item.quantity
        context["product_qty_in_cart"] = product_qty_in_cart
        return context


def product_main_image_view(request, *args, **kwargs):
    product_id = UUID(request.GET.get("product_id"))
    product = Product.objects.filter(id=product_id).prefetch_related("images").first()
    image_id = request.GET.get("image_id")
    if image_id:
        image_id = UUID(request.GET.get("image_id"))
        image = product.images.filter(id=image_id).first()
        context = {"product": product, "image": image}
    else:
        image = "main"
        context = {"product": product}
    return render(request, "categories/partials/product_main_image.html", context)


class ProductVideoView(DetailView):
    model = Product
    template_name = "categories/partials/product_video.html"


class PageNotFoundView(TemplateView):
    template_name = "errors/404.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context, status=404)


class BadRequestView(TemplateView):
    template_name = "errors/400.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({}, status=400)


class ForbiddenView(TemplateView):
    template_name = "errors/403.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({}, status=403)


class ServerErrorView(TemplateView):
    template_name = "errors/500.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({}, status=500)
