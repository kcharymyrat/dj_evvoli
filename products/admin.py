from django import forms
from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import Product, Category, ProductImage, ProductSpecification
from .mixins import ImageValidationMixin

max_image_resolution = ImageValidationMixin.MAX_RESOLUTIONS
min_image_resolution = ImageValidationMixin.MIN_RESOLUTIONS
max_image_size = ImageValidationMixin.MAX_IMAGE_SIZE


class CategoryAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = mark_safe(
            '<span style="color:red; font-size:12px;">'
            + _(f"Required resolution of the image should be within")
            + str(min_image_resolution)
            + _("and")
            + str(max_image_resolution)
            + "</span>"
        )


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = [
        "name",
        "slug",
        "products_count",
    ]
    readonly_fields = ["img_preview"]
    prepopulated_fields = {
        "slug": ("name_en",),
    }

    def products_count(self, obj):
        # Assuming 'products' is a reverse relation from a Product model
        return obj.products.count()

    products_count.short_description = _("Number of Products")


admin.site.register(Category, CategoryAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]
    search_fields = ["product__model"]
    readonly_fields = ["img_preview"]


admin.site.register(ProductImage, ProductImageAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ["img_preview"]
    extra = 0


class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]
    search_fields = ["product__model"]
    readonly_fields = ["title", "title_en", "title_ru"]


admin.site.register(ProductSpecification, ProductSpecificationAdmin)


class ProductSpecificationTitleInline(admin.StackedInline):
    model = ProductSpecification
    extra = 0
    fields = ["title", "title_en", "title_ru", "content", "content_en", "content_ru"]


class ProductAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = mark_safe(
            '<span style="color:green; font-size:12px;">'
            + _(f"Required resolution of the image should be within")
            + str(min_image_resolution)
            + _("and")
            + str(max_image_resolution)
            + "</span>"
        )


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "category",
        "type",
        "model",
        "in_stock",
        "price",
        "sale_percent",
        "sale_price",
    ]
    prepopulated_fields = {
        "slug": ("model",),
    }
    list_filter = [
        "category__name",
        "type",
    ]
    search_fields = [
        "type",
        "model",
        "category__name",
        "category__name_en",
        "category__name_ru",
    ]
    inlines = (ProductImageInline, ProductSpecificationTitleInline)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ("sale_price", "img_preview")


admin.site.register(Product, ProductAdmin)
