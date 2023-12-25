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


class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=8)
    delivery_time = serializers.DateTimeField()
    payment_option = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    cart = serializers.DictField(child=serializers.IntegerField())

    def create(self, validated_data):
        cart_data = validated_data.pop("cart")
        cart = Cart.objects.create()

        for product_id, quantity in cart_data.items():
            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise serializers.ValidationError(
                    f"Product with ID {product_id} does not exist"
                )
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        print("validated_data =", validated_data)
        order = Order.objects.create(cart=cart, **validated_data)
        return order
