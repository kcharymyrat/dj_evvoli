from .models import Category, Product


def categories(request):
    return {"categories": Category.objects.all()}


def product_types(request):
    types = set(Product.objects.values_list("type", flat=True).distinct())
    print(types)
    return {"product_types": types}
