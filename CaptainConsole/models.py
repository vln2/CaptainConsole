from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=999, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField()


class Address(models.Model):
    street = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class UserInfo(models.Model):
    admin = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT)


class Shipping(models.Model):
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    dateShipped = models.DateTimeField()
    trackingNumber = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    shippingCost = models.FloatField()


class Order(models.Model):
    dateCreated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT)

