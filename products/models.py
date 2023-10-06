import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from django.conf.global_settings import LANGUAGE_CODE

from PIL import Image

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

User = settings.AUTH_USER_MODEL


class ImageResolutionError(Exception):
    pass


class ImageSizeError(Exception):
    pass


class Category(models.Model):
    REQUIRED_RESOLUTIONS = (600, 600)
    MAX_IMAGE_SIZE = 12_900_000

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name (Turkmen)"), max_length=50, unique=True)
    name_en = models.CharField(_("name (English)"), max_length=50, unique=True)
    name_ru = models.CharField(_("name (Russian)"), max_length=50, unique=True)

    slug = models.SlugField(_("slug"), unique=True)

    description = models.TextField(_("description (Turkmen)"), null=True, blank=True)
    description_en = models.TextField(_("description (English)"), null=True, blank=True)
    description_ru = models.TextField(_("description (Russian)"), null=True, blank=True)

    image = models.ImageField(_("image"), upload_to="images/categories/")

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(
        User, verbose_name=_("created by"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("products:category_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        print("img.width =", img.width, "img.height =", img.height)
        width, height = self.REQUIRED_RESOLUTIONS
        # if image.size > Category.MAX_IMAGE_SIZE:
        #     raise ImageSizeError(
        #         _(
        #             f"Make sure that your image is less than {int(self.REQUIRED_RESOLUTIONS / 1_000_000)} MB!"
        #         )
        #     )
        # if img.width != width or img.height != height:
        #     raise ImageResolutionError(
        #         _(
        #             f"Please upload an image with correcr resolution: {self.REQUIRED_RESOLUTIONS}!"
        #         )
        #     )
        super().save(*args, **kwargs)


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()[:2]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        related_name="products",
    )

    type = models.CharField(_("type (Turkmen)"), max_length=50, null=True, blank=True)
    type_en = models.CharField(_("type (English)"), max_length=50, null=True, blank=True)
    type_ru = models.CharField(_("type (Russian)"), max_length=50, null=True, blank=True)

    model = models.CharField(_("model (Turkmen)"), max_length=100, unique=True)
    model_en = models.CharField(_("model (English)"), max_length=100, unique=True)
    model_ru = models.CharField(_("model (Russian)"), max_length=100, unique=True)

    title = models.CharField(_("title (Turkmen)"), max_length=100, unique=True)
    title_en = models.CharField(_("title (English)"), max_length=100, unique=True)
    title_ru = models.CharField(_("title (Russian)"), max_length=100, unique=True)

    slug = models.SlugField(_("slug"), unique=True)

    description = models.TextField(_("description (Turkmen)"), null=True, blank=True)
    description_en = models.TextField(_("description (English)"), null=True, blank=True)
    description_ru = models.TextField(_("description (Russian)"), null=True, blank=True)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(
        User, verbose_name=_("created by"), on_delete=models.CASCADE
    )

    objects = models.Manager()
    newest = ProductManager()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(_("image"), upload_to="images/products/")
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(width=200)],
        format="JPEG",
        options={"quality": 80},
    )
    description = models.CharField(
        _("description"), max_length=50, blank=True, null=True
    )

    @property
    def img_preview(self):
        return mark_safe(f'<img src = "{self.thumbnail.url}"/>')

    def __str__(self) -> str:
        return f"{self.product.title}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="specs",
    )
    title = models.CharField(_("title (Turkmen)"), max_length=255, unique=True)
    title_en = models.CharField(_("title (English)"), max_length=255, unique=True)
    title_ru = models.CharField(_("title (Russian)"), max_length=255, unique=True)
    content = models.CharField(_("content (Turkmen)"), max_length=255)
    content_en = models.CharField(_("content (English)"), max_length=255)
    content_ru = models.CharField(_("content (Russian)"), max_length=255)

    class Meta:
        verbose_name = _("product spec")
        verbose_name_plural = _("product specs")
