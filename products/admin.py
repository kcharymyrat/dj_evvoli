from django import forms
from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from PIL import Image

from .models import Product, Category, ProductImage, ProductSpecification


class CategoryAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = mark_safe(
            '<span style="color:red; font-size:12px;">'
            + _(f"Required resolution of the image")
            + "</span>"
        )


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ["name", "slug"]
    readonly_fields = ["img_preview"]
    prepopulated_fields = {
        "slug": ("name_en",),
    }


admin.site.register(Category, CategoryAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]
    search_fields = ["product"]
    readonly_fields = ["img_preview"]


admin.site.register(ProductImage, ProductImageAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ["img_preview"]
    extra = 0


class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ["id", "product"]
    search_fields = ["product"]
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
            '<span style="color:red; font-size:12px;">'
            + _(f"Required resolution of the image are")
            + "</span>"
        )


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "type",
        "title",
        "model",
        "slug",
        "price",
        "sale_percent",
        "sale_price",
    ]
    prepopulated_fields = {
        "slug": ("title_en",),
    }
    list_filter = ["type", "title", "model", "price", "created_by"]
    search_fields = ["type", "created_by"]
    inlines = (ProductImageInline, ProductSpecificationTitleInline)

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ("sale_price", "img_preview")


admin.site.register(Product, ProductAdmin)
