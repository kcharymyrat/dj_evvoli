from rest_framework import serializers

from products.models import Category, Product, ProductImage, ProductSpecification
from orders.models import CartItem, Cart, Order


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


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id"]


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField(source="product.id", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "product_id",
            "quantity",
        ]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "cart_items",
        ]
