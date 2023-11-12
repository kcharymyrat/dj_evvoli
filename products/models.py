import uuid

from decimal import Decimal
from PIL import Image
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from django.db import models
from django.db.models import CheckConstraint, Q
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf.global_settings import LANGUAGE_CODE

from .mixins import ImageValidationMixin, VideoValidationMixin


User = settings.AUTH_USER_MODEL


class Category(ImageValidationMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name (Turkmen)"), max_length=50, unique=True)
    name_en = models.CharField(_("name (English)"), max_length=50, unique=True)
    name_ru = models.CharField(_("name (Russian)"), max_length=50, unique=True)

    slug = models.SlugField(_("slug"), unique=True)

    description = models.TextField(_("description (Turkmen)"), null=True, blank=True)
    description_en = models.TextField(_("description (English)"), null=True, blank=True)
    description_ru = models.TextField(_("description (Russian)"), null=True, blank=True)

    image = models.ImageField(_("image"), upload_to=f"images/categories/")
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(width=400)],
        format="JPEG",
        options={"quality": 80},
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    modified_at = models.DateTimeField(_("modified at"), auto_now=True)
    created_by = models.ForeignKey(
        User, verbose_name=_("created by"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = ["-created_at"]

    @property
    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}"/>')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("products:category_detail", kwargs={"slug": self.slug})

    def clean(self):
        """Validation for the image, before saving."""
        super().clean()
        self.clean_image()


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()[:10]


class Product(ImageValidationMixin, VideoValidationMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        related_name="products",
        db_index=True,
    )

    type = models.CharField(_("type (Turkmen)"), max_length=50, null=True, blank=True)
    type_en = models.CharField(
        _("type (English)"), max_length=50, null=True, blank=True
    )
    type_ru = models.CharField(
        _("type (Russian)"), max_length=50, null=True, blank=True
    )

    model = models.CharField(_("model"), max_length=100, unique=True, db_index=True)

    title = models.CharField(_("title (Turkmen)"), max_length=100, unique=True)
    title_en = models.CharField(_("title (English)"), max_length=100, unique=True)
    title_ru = models.CharField(_("title (Russian)"), max_length=100, unique=True)

    slug = models.SlugField(_("slug"), unique=True)

    price = models.DecimalField(_("price"), max_digits=6, decimal_places=2)
    sale_percent = models.PositiveIntegerField(
        _("sale percentage"), default=0, validators=[MaxValueValidator(100)]
    )
    sale_price = models.DecimalField(
        _("sale price"), max_digits=6, decimal_places=2, blank=True, null=True
    )
    on_sale = models.BooleanField(_("on sale"), default=False, db_index=True)

    description = models.TextField(_("description (Turkmen)"), null=True, blank=True)
    description_en = models.TextField(_("description (English)"), null=True, blank=True)
    description_ru = models.TextField(_("description (Russian)"), null=True, blank=True)

    in_stock = models.BooleanField(_("in stock"), default=True)

    image = models.ImageField(_("image"), upload_to=f"images/products/")
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(width=400)],
        format="JPEG",
        options={"quality": 80},
    )
    video = models.FileField(
        _("video"), upload_to="videos/products/", null=True, blank=True
    )

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
        constraints = [
            CheckConstraint(
                check=Q(sale_percent__gte=0, sale_percent__lte=100),
                name="sale_percent_between_0_and_100",
            )
        ]

    @property
    def img_preview(self):
        return mark_safe(f'<img src = "{self.image.url}"/>')

    def clean(self):
        """Validation for the image, before saving."""
        super().clean()
        self.clean_image()
        if self.video:
            self.clean_video()

    def save(self, *args, **kwargs):
        if self.sale_percent > 0:
            self.on_sale = True
            self.sale_price = Decimal(
                "%.2f" % (self.price * (100 - self.sale_percent) / 100)
            )
        elif self.sale_percent == 0:
            self.sale_price = self.price
            self.on_sale = False
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Product: {self.title}, price: {self.price}"

    # def get_absolute_url(self):
    #     return reverse("products:product_detail", kwargs={"slug": self.slug})

    # def clean(self):
    #     """
    #     Validation for the video.
    #     """
    #     super().clean()
    #     if self.video:
    #         if self.video.file.content_type not in [
    #             "video/mp4",
    #             "video/quicktime",
    #             "video/x-matroska",
    #         ]:
    #             raise ValidationError(
    #                 {
    #                     "video": _(
    #                         "Unsupported file type. Only mp4, quicktime, and mkv are supported."
    #                     )
    #                 }
    #             )
    #         if self.video.size > 20 * 1024 * 1024:
    #             raise ValidationError(
    #                 {"video": _("Video file too large. Maximum size is 20MB.")}
    #             )


class ProductImage(ImageValidationMixin, models.Model):
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
        processors=[ResizeToFit(width=400)],
        format="JPEG",
        options={"quality": 80},
    )
    description = models.CharField(
        _("description"), max_length=50, blank=True, null=True
    )

    @property
    def img_preview(self):
        return mark_safe(f'<img src = "{self.thumbnail.url}"/>')

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")

    def clean(self):
        """Validation for the image, before saving."""
        super().clean()
        self.clean_image()

    def __str__(self) -> str:
        return f"{self.product.title}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="specs",
    )
    title = models.CharField(_("title (Turkmen)"), max_length=255)
    title_en = models.CharField(_("title (English)"), max_length=255)
    title_ru = models.CharField(_("title (Russian)"), max_length=255)
    content = models.CharField(_("content (Turkmen)"), max_length=255)
    content_en = models.CharField(_("content (English)"), max_length=255)
    content_ru = models.CharField(_("content (Russian)"), max_length=255)

    class Meta:
        verbose_name = _("product specification")
        verbose_name_plural = _("product specifications")
