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
    regex=r"^\d{6}$",
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
        cart = self.cart
        super().delete(*args, **kwargs)  # Call the "real" delete() method.
        cart.update_total_price()  # Update the cart's total price after deletion.

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
        max_length=6,
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
        self.cart.update_is_order()
        return super().save()

    def __str__(self):
        return f"{self.id}, order_price = {self.total_order_price}"


# Order and Cart Imlementation

"""
Based on your provided models, I'll create `Cart` and `Order` models. The `Cart` model will contain an ID, a list of products, and a total price. The `Order` model will contain an ID, a reference to the cart, a status, and a timestamp. 

Here is how you could define these models:

```python
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    products = models.ManyToManyField(Product, through='CartProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.id)


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

        
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
```

In these models, `CartProduct` is a through model for the many-to-many relationship between `Cart` and `Product`. 
This allows us to store additional information about the relationship, such as the quantity of each product in the cart.
The `Order` model has a one-to-one relationship with `Cart`, meaning each order is associated with exactly one cart. 
The status of the order is stored as a string, with several possible values represented as choices.

Please note that these models are quite basic and might not cover all the functionalities you would need 
in a real-world application, such as handling discounts, taxes, shipping costs, user addresses, etc.
"""

"""
class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product


class Order(models.Model):
    ORDER_STATUSES = (
        ('Created', 'Created'),
        ('Paid', 'Paid'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=120, unique=True, default=uuid.uuid4)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, choices=ORDER_STATUSES, default='Created')
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
"""
