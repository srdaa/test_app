from django.db import models

# Create your models here.


class Item(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField()
    price = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = "Модель Item"

class Order(models.Model):
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    items = models.ManyToManyField(Item, through='OrderItem')

    class Meta:
        verbose_name = "Заказы"

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Связующая таблица"