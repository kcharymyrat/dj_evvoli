import uuid

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.conf.global_settings import LANGUAGE_CODE

from products.models import Product

User = settings.AUTH_USER_MODEL

# TODO: Orgonize the Cart and Order so the Cart is no longer available or has a status changed to ordered


class Cart(models.Model):
    products = models.ManyToManyField(
        Product, verbose_name=_("products"), through="CartItem"
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
        self.total_price = sum(item.sub_total for item in self.cartitem_set.all())
        self.save()

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, verbose_name=_("product"), on_delete=models.CASCADE
    )
    cart = models.ForeignKey(Cart, verbose_name=_("cart"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("quantity"), default=1)

    @property
    def sub_total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("carts items")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        self.cart.update_total_price()  # Update the cart's total price after saving.

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


class Order(models.Model):
    ORDER_STATUSES = (
        (_("Created"), _("Created")),
        (_("Ordered"), _("Ordered")),
    )

    user = models.ForeignKey(
        User, verbose_name=_("user"), on_delete=models.CASCADE, null=True, blank=True
    )
    cart = models.ForeignKey(Cart, verbose_name=_("cart"), on_delete=models.CASCADE)
    status = models.CharField(
        _("status"), max_length=120, choices=ORDER_STATUSES, default="Created"
    )
    total_order_price = models.DecimalField(
        _("total order price"), default=0.00, max_digits=100, decimal_places=2
    )
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ["-timestamp"]

    def save(self) -> None:
        self.total_order_price = self.cart.total_price
        self.cart.is_ordered = True
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
