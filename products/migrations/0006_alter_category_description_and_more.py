# Generated by Django 4.2.6 on 2024-01-14 13:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_alter_product_type_alter_product_type_en_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(
                default="Category description", verbose_name="description (Turkmen)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="description_en",
            field=models.TextField(
                default="Category descripttion en", verbose_name="description (English)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="description_ru",
            field=models.TextField(
                default="Category description ru", verbose_name="description (Russian)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(
                default="Description", verbose_name="description (Turkmen)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="description_en",
            field=models.TextField(
                default="Description en", verbose_name="description (English)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="description_ru",
            field=models.TextField(
                default="Description rr", verbose_name="description (Russian)"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.UUIDField(
                db_index=True,
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="title",
            field=models.CharField(max_length=100, verbose_name="title (Turkmen)"),
        ),
        migrations.AlterField(
            model_name="product",
            name="title_en",
            field=models.CharField(max_length=100, verbose_name="title (English)"),
        ),
        migrations.AlterField(
            model_name="product",
            name="title_ru",
            field=models.CharField(max_length=100, verbose_name="title (Russian)"),
        ),
        migrations.AlterField(
            model_name="product",
            name="type",
            field=models.CharField(
                db_index=True, max_length=50, null=True, verbose_name="type (Turkmen)"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="type_en",
            field=models.CharField(
                db_index=True, max_length=50, null=True, verbose_name="type (English)"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="type_ru",
            field=models.CharField(
                db_index=True, max_length=50, null=True, verbose_name="type (Russian)"
            ),
        ),
    ]
