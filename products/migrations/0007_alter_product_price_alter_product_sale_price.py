# Generated by Django 4.2.6 on 2024-01-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_alter_category_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                db_index=True, decimal_places=2, max_digits=10, verbose_name="price"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="sale_price",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=10,
                null=True,
                verbose_name="sale price",
            ),
        ),
    ]
