from django.contrib import admin

from .models import CartItem, Cart, Order


class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "total_price", "is_ordered", "get_cart_items"]
    list_display_links = ["get_cart_items"]
    readonly_fields = ["total_price", "is_ordered", "get_cart_items"]

    def get_cart_items(self, instance):
        return [cart_item for cart_item in instance.cart_items.all()]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "cart",
        "status",
        "delivery_time",
        "payment_option",
        "customer_name",
        "phone",
        "shipping_address",
        "total_order_price",
        "all_cart_items",
    ]
    list_filter = ["status", "phone", "payment_option"]
    readonly_fields = ("total_order_price",)
    list_display_links = ["cart"]
    list_editable = ["status"]

    def get_cart_items(self, instance):
        return [cart for cart in instance.carts.all()]

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ("all_cart_items",)


admin.site.register(CartItem)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
