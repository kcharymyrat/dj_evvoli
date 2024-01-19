from django.contrib import admin

from .models import CartItem, Cart, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Removes the extra empty fields

    def has_change_permission(self, request, obj=None):
        # Returning False will make the inline items non-editable
        return False

    def has_add_permission(self, request, obj=None):
        # Returning False will prevent adding new inline items
        return False

    def has_delete_permission(self, request, obj=None):
        # Returning False will prevent deleting inline items
        return False


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ["id", "total_price", "is_ordered", "get_cart_items"]
    list_display_links = ["id", "get_cart_items"]
    readonly_fields = ["total_price", "is_ordered", "get_cart_items"]

    def get_cart_items(self, instance):
        return [cart_item for cart_item in instance.cart_items.all()]

    def has_change_permission(self, request, obj=None):
        # Returning False will make the inline items non-editable
        return False

    def has_add_permission(self, request, obj=None):
        # Returning False will prevent adding new inline items
        return False

    def has_delete_permission(self, request, obj=None):
        # Returning False will prevent deleting inline items
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Removes the extra empty fields

    def has_change_permission(self, request, obj=None):
        # Returning False will make the inline items non-editable
        return False

    def has_add_permission(self, request, obj=None):
        # Returning False will prevent adding new inline items
        return False

    def has_delete_permission(self, request, obj=None):
        # Returning False will prevent deleting inline items
        return False


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
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
    ]

    readonly_fields = (
        "id",
        "cart",
        "delivery_time",
        "payment_option",
        "customer_name",
        "phone",
        "email",
        "shipping_address",
        "total_order_price",
        "all_order_items",
    )
    list_filter = ["status", "payment_option"]
    search_fields = (
        "phone",
        "customer_name",
    )
    list_display_links = ["id"]

    def has_add_permission(self, request, obj=None):
        # Returning False will prevent adding new inline items
        return False

    def has_delete_permission(self, request, obj=None):
        # Returning False will prevent deleting inline items
        return False


admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
