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
    return _search_results_view(request, products)


def _search_results_view(request, products):
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "products/search_results.html", context)


def specific_category_products(request, slug):
    category_products = Category.objects.filter(slug=slug).first().products.all()
    return _specific_category_products_view(request, category_products)


def _specific_category_products_view(request, category_products):
    paginator = Paginator(category_products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "category_name": category_products.first().category.name,
        "category_name_en": category_products.first().category.name_en,
        "category_name_ru": category_products.first().category.name_ru,
    }
    return render(request, "products/category_detail.html", context)


class HomeTemplateView(TemplateView):
    template_name = "index_trial.html"


class ProductListView(ListView):
    model = Product
    paginate_by = 12
    context_object_name = "products"
    template_name = "products/products_trial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
