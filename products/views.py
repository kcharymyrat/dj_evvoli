from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Category, Product


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
        return "index_trial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


products_global = Product.objects.all()


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = "products"

    def get_template_names(self):
        print("products:", self.queryset)
        if self.request.htmx:
            print("HTMX request triggered")
            return "products/components/product_list_elements.html"
        products_global = Product.objects.all()
        return "products/products_trial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        global products_global

        request = self.request
        print()
        print("---------------------")
        print(f"request.GET = {request.GET}")
        print(f"request.POST = {request.POST}")
        print(
            f"request.htmx.current_url_abs_path = {request.htmx.current_url_abs_path}"
        )
        print(f"request.htmx.current_url = {request.htmx.current_url}")
        print(f"request.htmx.target = {request.htmx.target}")
        print(f"request.htmx.trigger = {request.htmx.trigger}")
        print(f"request.htmx.trigger_name = {request.htmx.trigger_name}")
        print(f"request.htmx.triggering_event = {request.htmx.triggering_event}")
        print("--------------------\n\n\n")

        {(product.type, product.model) for product in products_global}

        if request.htmx.trigger == "product_type_form":
            print("in request.htmx.trigger == product_type_form")

            product_type = request.GET.get("product_type")
            products_global = Product.objects.filter(type=product_type)
            print(f"product_type ={product_type}, {type(product_type)}")

            # Check if all product types was chose
            if product_type == "all":
                print('in product_type == "all"')
                products_global = Product.objects.all()

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
