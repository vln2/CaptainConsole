from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', db_index=True)
    slug = models.SlugField()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug')
        verbose_name_plural = 'categories'

    def get_slug_list(self):
        ancestors = []
        slugs = []

        try:
            ancestors = self.get_ancestors(include_self=True)
        finally:
            ancestors = [i.slug for i in ancestors]
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))

        return slugs

    def get_slug_link(self):
        slugs = self.get_slug_list()
        if slugs:
            return slugs[-1]

    def get_products(self, sort_by=None):
        descendants = self.get_descendants(include_self=True)
        # descendants = [i.name for i in descendants]
        if sort_by != None:
            return Product.objects.order_by(sort_by).filter(category__in=descendants)

        return Product.objects.filter(category__in=descendants)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = TreeForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField()
    slug = models.SlugField(null=False)
    thumb = models.ImageField(upload_to='images/thumbs/', default='No_image_available.png', blank=True)
    # discount = models.IntegerField( default=0 ) 

    def __str__(self):
        return self.name

    # def valid_discound(self):
    #     """Checks if the discount is valid (not higher than actual price)"""
    #     if discount > price or discount == 0:
    #         return False
    #     else:
    #         return True


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/products/')

    def __str__(self):
        return str(self.product.id)


class Address(models.Model):
    street = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.email


class Shipping(models.Model):
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    dateShipped = models.DateTimeField()
    trackingNumber = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    shippingCost = models.FloatField()


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    dateCreated = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField(Item)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT, null=True)
    CART = 'C'
    order_labels = (
        (CART, 'Cart'),
        ('P', 'Payment'),
        ('S', 'Shipping'),
        ('D', 'Done')
    )
    status = models.CharField(choices=order_labels, max_length=1, default='C')

    def __str__(self):
        return self.owner.username

    def getTotal(self):
        order_sum = 0
        for item in self.items.all():
            order_sum += item.product.price
        return round(order_sum, 2)
