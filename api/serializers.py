import logging

from django.db import transaction

from rest_framework import serializers

from products.models import Category, Product, ProductImage, ProductSpecification
from orders.models import CartItem, Cart, Order, OrderItem

api_logger = logging.getLogger("api")


class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "name_en",
            "name_ru",
            "slug",
            "description",
            "description_en",
            "description_ru",
            "image_url",
            "thumbnail_url",
        ]
        read_only_fields = fields  # Make all fields read-only

    def get_image_url(self, obj):
        return obj.image.url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail.url


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source="category.id", read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category_id",
            "type",
            "type_en",
            "type_ru",
            "model",
            "title",
            "title_en",
            "title_ru",
            "slug",
            "price",
            "sale_percent",
            "sale_price",
            "on_sale",
            "in_stock",
            "image_url",
            "thumbnail_url",
        ]
        read_only_fields = fields  # Make all fields read-only

    def get_image_url(self, obj):
        return obj.image.url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail.url


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image_url",
            "thumbnail_url",
            "description",
        ]

    def get_image_url(self, obj):
        return obj.image.url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail.url


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = [
            "id",
            "title",
            "title_en",
            "title_ru",
            "content",
            "content_en",
            "content_ru",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(source="category.id", read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    video_url = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category_id",
            "type",
            "type_en",
            "type_ru",
            "model",
            "title",
            "title_en",
            "title_ru",
            "slug",
            "price",
            "sale_percent",
            "sale_price",
            "on_sale",
            "description",
            "description_en",
            "description_ru",
            "in_stock",
            "image_url",
            "thumbnail_url",
            "video_url",
            "images",
            "specs",
        ]

    def get_image_url(self, obj):
        return obj.image.url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail.url

    def get_video_url(self, obj):
        if obj.video and hasattr(obj.video, "url"):
            return obj.video.url
        return None


class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=8)
    shipping_address = serializers.CharField()
    delivery_time = serializers.DateTimeField()
    payment_option = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    cart = serializers.DictField(child=serializers.IntegerField())

    def create(self, validated_data):
        print("validated_data =", validated_data)
        with transaction.atomic():
            cart_data = validated_data.pop("cart")
            # Check if cart_data is empty
            if not cart_data:
                raise serializers.ValidationError(
                    {"detail": "No product data provided for order creation."}
                )

            # Create the Order with all the validated data
            order = Order.objects.create(**validated_data)

            for product_id, quantity in cart_data.items():
                try:
                    product = Product.objects.get(id=product_id)

                    OrderItem.objects.create(
                        order=order,
                        product_title=product.title,
                        product_model=product.model,
                        product_price=product.sale_price,
                        quantity=quantity,
                    )

                except Product.DoesNotExist as e:
                    api_logger.error(
                        f"Order FAILED since no product with id = {product_id} : {e}"
                    )
                    raise serializers.ValidationError(
                        {
                            "detail": f"Product does not exist",
                            "product_id": product_id,
                        }
                    )

                except Exception as e:
                    api_logger.error(f"Error creating order: {e}")
                    raise serializers.ValidationError(
                        {"detail": f"An error occurred while creating the order."}
                    )

            order.update_total_price()

        print("validated_data =", validated_data)
        return order
