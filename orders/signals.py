from django.db.models.signals import pre_delete
from django.dispatch import receiver
from products.models import Product  # Import Product model from the products app


@receiver(pre_delete, sender=Product)
def update_cart_before_product_delete(sender, instance, **kwargs):
    for cart_item in instance.cart_items.all():
        cart_item.delete()
