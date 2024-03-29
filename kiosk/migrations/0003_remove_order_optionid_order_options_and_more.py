# Generated by Django 4.2.5 on 2024-02-14 21:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kiosk", "0002_cart_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="optionId",
        ),
        migrations.AddField(
            model_name="order",
            name="options",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name="order",
            name="menuId",
        ),
        migrations.AddField(
            model_name="order",
            name="menuId",
            field=models.ManyToManyField(blank=True, to="kiosk.menu"),
        ),
    ]