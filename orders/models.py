from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.

class Payment(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    payment_id      = models.CharField(max_length=100)
    payment_method  = models.CharField(max_length=100)
    amount_paid     = models.CharField(max_length=100)
    status          = models.CharField(max_length=100)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ('Processing','Processing'),
        ('Accepted','Accepted'),
        ('Out For Delivery','Out For Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )

    user            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number    = models.CharField(max_length=30)
    first_name      = models.CharField(max_length=40)
    last_name       = models.CharField(max_length=40) 
    email           = models.EmailField(max_length=30)
    phone           = models.CharField(max_length=20)
    address_1       = models.CharField(max_length=60)
    address_2       = models.CharField(max_length=60, blank=True)
    country         = models.CharField(max_length=40)
    state           = models.CharField(max_length=40)
    city            = models.CharField(max_length=40)
    order_note      = models.CharField(max_length=60, blank=True)
    order_total     = models.FloatField()
    tax             = models.FloatField()
    status          = models.CharField(max_length=25, choices=STATUS, default='Processing')
    ip_address      = models.CharField(max_length=20, blank=True)
    is_ordered      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
class OrderProduct(models.Model):
    STATUS = (
        ('Processing','Processing'),
        ('Accepted','Accepted'),
        ('Out For Delivery','Out For Delivery'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
    )

    order           = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    payment         = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user            = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity        = models.IntegerField()
    product_price   = models.FloatField()
    status          = models.CharField(max_length=25, choices=STATUS, default='Processing')
    ordered         = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name


class OrderTracking(models.Model):
    order       = models.ForeignKey(OrderProduct, on_delete=models.CASCADE, null=True)
    accepted  = models.CharField(max_length=30, blank=True)
    a_date      = models.DateTimeField(null=True, blank=True)
    out_delivery  = models.CharField(max_length=30, blank=True)
    out_date      = models.DateTimeField(null=True, blank=True)
    delivered  = models.CharField(max_length=20, blank=True)
    d_date      = models.DateTimeField(null=True, blank=True)
    cancelled  = models.CharField(max_length=30, blank=True)
    c_date      = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.order.status



