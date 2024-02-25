from django.db import models
from django.contrib.auth.models import AbstractUser


class Store(AbstractUser) :
    phone = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Store'

class Category(models.Model):
    categoryId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name}'

class Menu(models.Model):
    menuId = models.BigAutoField(primary_key=True)
    storeId = models.ForeignKey(Store, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Category, on_delete=models.RESTRICT, null=True)
    name = models.CharField(max_length=255)
    optionId = models.ManyToManyField('Option', blank=True)
    price = models.IntegerField()
    menuImg = models.ImageField(upload_to='kiosk/menu_images/%Y/%m/%d/', null=True, blank=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.name}'

class Option(models.Model):
    optionId = models.BigAutoField(primary_key=True)
    menuId = models.ForeignKey(Menu, on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    contents = models.ManyToManyField('OptionContent', blank=True)
    price = models.IntegerField()
    status = models.IntegerField(default=1)
    button = models.BooleanField(default=1)

    def __str__(self):
        return f'{self.option}'

class OptionContent(models.Model):
    content = models.CharField(max_length=255, null=True)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.content}'

class Cart(models.Model):
    cartId = models.BigAutoField(primary_key=True)
    menuId = models.ForeignKey(Menu, on_delete=models.CASCADE)
    options =  models.TextField(null=True, blank=True)
    price = models.IntegerField()
    # quantity = models.IntegerField(default=1)
    type = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.menuId.name}'

class Order(models.Model):
    orderId = models.BigAutoField(primary_key=True)
    menuId = models.ManyToManyField('Menu', blank=True)
    options =  models.TextField(null=True, blank=True)
    pay = models.CharField(max_length=255)
    totalPrice = models.IntegerField()
    totalQuantity = models.IntegerField()
    date = models.DateField(auto_now_add = True)

    def __str__(self):
        return f'[{self.pk}]'