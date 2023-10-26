from django.db import models
from .forms import *
from django.contrib.auth.models import User
from django.views import View
import datetime
from django.shortcuts import redirect
from django.http import HttpResponseRedirect



class Contact (models.Model):
    contact_id = models.AutoField(primary_key=True)
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_subject = models.TextField(max_length=2000,  null=True, blank=True)
    contact_email = models.EmailField(max_length=100,  null=True, blank=True)
    contact_message = models.TextField(max_length=5000, null=True, blank=True )

    def _str_(self):
        return f'{self.contact_name}'


class Articles(models.Model):
    articles_id = models.AutoField(primary_key=True)
    articles_image = models.ImageField(upload_to="article/",null=True, blank=True)
    articles_category = models.CharField(max_length=50, null=True, blank=True)
    articles_written = models.CharField(max_length=50, null=True, blank=True)
    articles_title = models.CharField(max_length=100, null=True, blank=True)
    articles_update = models.CharField(max_length=100, null=True, blank=True)
    articles_subtitle = models.CharField(max_length=100, null=True, blank=True)
    articles_info = models.TextField(max_length=8000, null=True, blank=True)
    articles_description = models.TextField(max_length=2000, null=True, blank=True)
    articles_hashtag = models.TextField(max_length=500, null=True, blank=True)

    def _str_(self):
        return f"{self.articles_title}"
    

# SHOP / ADD TO CART

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_image = models.ImageField(null=True,upload_to="product/")
    product_image1 = models.ImageField(upload_to="product/", null=True, blank=True)
    # product_image2 = models.ImageField(upload_to="product/", null=True, blank=True)
    # product_image3 = models.ImageField(upload_to="product/", null=True, blank=True)
    product_title = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    product_digital = models.BooleanField(default=False,null=True,blank=False)
    product_description = models.TextField(max_length=5000, null=True, blank=True)
    
    def _str_(self):
        return f"{self.products_title}"
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url  
    
    # fuksioni i totalit per produkt
    def get_total(self):
        total = self.item.product_price * self.quantity
        float_total = format(total, '0.2f')
        return float_total


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    # fuksioni i totalit per te gjitha produktet e cart
    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            # get_total - funksion i ndertuar me lart
            total += float(order_item.get_total())
        return total



class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True,null=True)
    address = models.CharField(max_length=200,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    state = models.CharField(max_length=200,null=True,blank=True)
    zipcode = models.IntegerField( null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address




















