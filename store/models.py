from django.db import models
from django.urls import reverse
from accounts.models import Account

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=200,null=True,blank=True)
    category_image=models.ImageField(upload_to='images/category',null=True,blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_category_slug(self):
        return reverse('category_products',args=[self.slug])
    
    def __str__(self):
        return self.category_name
    


class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    price=models.IntegerField()
    stock=models.IntegerField()
    product_image=models.ImageField(upload_to='images/products',null=True,blank=True)
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    in_wishlist = models.BooleanField(default=False,null=True,blank=True)

    def get_product_cat_slug(self):
        return reverse('product_details',args=[self.category.slug ,self.slug])

    def __str__(self):
        return self.product_name
    
