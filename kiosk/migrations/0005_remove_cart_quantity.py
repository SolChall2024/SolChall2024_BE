# Generated by Django 4.2.5 on 2024-02-15 01:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("kiosk", "0004_alter_order_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="quantity",
        ),
    ]