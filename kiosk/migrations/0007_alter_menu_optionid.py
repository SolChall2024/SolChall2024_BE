# Generated by Django 5.0.2 on 2024-02-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0006_category_remove_menu_category_menu_categoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='optionId',
            field=models.ManyToManyField(blank=True, to='kiosk.option'),
        ),
    ]