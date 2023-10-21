from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Category, Product


class HomeTemplateView(TemplateView):
    template_name = "index_trial.html"


class ProductTemplateView(TemplateView):
    template_name = "products/products_trial.html"
