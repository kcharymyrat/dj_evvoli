from django.db.models import Q
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


class ProductListView(ListView):
    model = Product
    paginate_by = 2
    context_object_name = "products"

    def get_template_names(self):
        if self.request.htmx:
            print("HTMX requwst triggered")
            return "products/components/product_list_elements.html"
        return "products/products_trial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
