import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django.conf.global_settings import LANGUAGE_CODE

from products.models import Product

User = settings.AUTH_USER_MODEL

phone_regex = RegexValidator(
    regex=r"^\d{8}$",
    message=_(
        "Phone number must be entered in the format: '12345678'. Exactly 8 digits."
    ),
)


class Cart(models.Model):
    products = models.ManyToManyField(
        Product,
        verbose_name=_("products"),
        through="CartItem",
        related_name="carts",
    )
    total_price = models.DecimalField(
        _("cart price"), max_digits=10, decimal_places=2, default=0.00
    )
    is_ordered = models.BooleanField(_("is ordered"), default=False)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    date_modified = models.DateTimeField(_("date added"), auto_now=True)

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.cart_items.all())

    class Meta:
        verbose_name = _("cart")
        verbose_name_plural = _("carts")
        ordering = ["date_added"]

    def update_total_price(self):
        self.total_price = sum(item.sub_total for item in self.cart_items.all())
        self.save()

    def update_is_order(self):
        self.is_ordered = True
        self.save()

    def __str__(self):
        return f"Cart {self.id}: {self.total_price} manats"


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("cart"),
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(_("quantity"), default=1)

    @property
    def sub_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("carts items")

    def save(self, *args, **kwargs):
        # If quantity is 0, delete the CartItem
        if self.quantity == 0:
            self.delete()
        else:
            super().save(*args, **kwargs)  # Call the "real" save() method.
            self.cart.update_total_price()  # Update the cart's total price after saving.

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)  # Call the "real" delete() method.
        self.cart.update_total_price()  # Update the cart's total price after deletion.

    def __str__(self):
        return f"{self.quantity}-{self.product.title} = {self.sub_total}"


class Order(models.Model):
    ORDER_STATUSES = (
        (_("Created"), _("Created")),
        (_("Ordered"), _("Ordered")),
        (_("Shipped"), _("Shipped")),
        (_("Completed"), _("Completed")),
        (_("Cancelled"), _("Cancelled")),
    )
    PAYMENT_CHOICES = (
        (_("Cash"), _("Cash")),
        (_("Card Terminal"), _("Card Terminal")),
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="order",
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("cart"),
        on_delete=models.CASCADE,
        related_name="order",
    )
    status = models.CharField(
        _("status"), max_length=120, choices=ORDER_STATUSES, default="Created"
    )
    payment_option = models.CharField(
        _("payment option"), max_length=120, choices=PAYMENT_CHOICES, default="Cash"
    )
    customer_name = models.CharField(_("customer name"), max_length=255)
    phone = models.CharField(
        _("phone number"),
        validators=[phone_regex],
        max_length=8,
        help_text=_("8 digits"),
    )
    delivery_time = models.DateTimeField(
        _("delivery date and time"), auto_now=False, auto_now_add=False
    )
    shipping_address = models.TextField(_("shipping address"))
    email = models.EmailField(_("email"), max_length=254, null=True, blank=True)
    total_order_price = models.DecimalField(
        _("total order price"), default=0.00, max_digits=100, decimal_places=2
    )
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-timestamp"]

    @property
    def all_cart_items(self):
        return [cart_item for cart_item in self.cart.cart_items.all()]

    def save(self) -> None:
        self.total_order_price = self.cart.total_price
        self.cart.update_is_ordered()
        return super().save()

    def __str__(self):
        return f"{self.id}, order_price = {self.total_order_price}"
