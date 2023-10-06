from django.contrib import admin
from django.forms import ModelForm, ValidationError
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from PIL import Image
from imagekit.admin import AdminThumbnail

from .models import Product, Category, ProductImage, ProductSpecification


class CategoryAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].help_text = mark_safe(
            '<span style="color:red; font-size:12px;">'
            + _(f"Required resolution of the image are {Category.REQUIRED_RESOLUTIONS}")
            + "</span>"
        )

    def clean_image(self):
        image = self.cleaned_data.get("image")
        img = Image.open(image)
        print(
            "img.width =",
            img.width,
            "img.height =",
            img.height,
            "image.size =",
            image.size,
        )
        # width, height = Category.REQUIRED_RESOLUTIONS
        # if image.size > Category.MAX_IMAGE_SIZE:
        #     raise ValidationError(
        #         _(
        #             f"Make sure that your image is less than {int(Category.REQUIRED_RESOLUTIONS / 1_000_000)} MB!"
        #         )
        #     )
        # if img.width = width or img.height != height:
        #     raise ValidationError(
        #         _(
        #             f"Please upload an image with correcr resolution: {Category.REQUIRED_RESOLUTIONS}!"
        #         )
        #     )
        return image


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ["name", "slug"]
    prepopulated_fields = {
        "slug": ("name",),
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


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "model", "slug", "created_at"]
    prepopulated_fields = {
        "slug": ("title",),
        "model_en": ("model",),
        "model_ru": ("model",),
    }
    list_filter = ["title", "model", "created_by", "created_at"]
    search_fields = ["title", "model", "created_by"]
    inlines = (ProductImageInline, ProductSpecificationTitleInline)


admin.site.register(Product, ProductAdmin)
