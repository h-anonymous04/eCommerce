from django.db import models
import os

c = (
    ("INR", "INR"),
    ("USD", "USD")
)

class Item(models.Model):
    item_image = models.ImageField(upload_to="items_images")
    item_name = models.CharField(max_length=200)
    item_description = models.TextField()
    item_price = models.FloatField()
    item_price_currency = models.CharField(choices=c, max_length=5)
    added_by = models.CharField(max_length=100)
    item_id = models.CharField(max_length=36)


class Order(models.Model):
    order_id = models.CharField(max_length=36)
    order_price_currency = models.CharField(max_length=5)
    order_price = models.FloatField()
    order_name = models.CharField(max_length=200)
    ordered_on = models.DateTimeField(auto_now_add=True)
    order_address = models.TextField()
    order_state = models.CharField(choices=(("p", "Pending"), ("a", "Accepted"), ("d", "Delivered"), ("o", "On the way")), max_length=1, default="p")
    item_id = models.CharField(max_length=36)
    ordered_by = models.CharField(max_length=100)
    order_item_from = models.CharField(max_length=100)