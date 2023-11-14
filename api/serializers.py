from rest_framework import serializers

from products.models import Category, Product, ProductImage, ProductSpecification


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
            "title",
            "title_en",
            "title_ru",
            "content",
            "content_en",
            "content_ru",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specs = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
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
            "video",
            "images",
            "specs",
        ]

    def get_image_url(self, obj):
        return obj.image.url

    def get_thumbnail_url(self, obj):
        return obj.thumbnail.url
