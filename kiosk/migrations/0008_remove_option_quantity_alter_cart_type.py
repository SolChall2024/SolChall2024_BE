# Generated by Django 5.0.2 on 2024-02-20 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0007_alter_menu_optionid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='cart',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]