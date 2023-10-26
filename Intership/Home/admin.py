from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_title','product_price','product_image']

# @admin.register(Customer)
# class CustomerModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user','email']
# customer duhet tlidhet me order dhe order me cart
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Contact)

@admin.register(ShippingAddress)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = []

admin.site.register(Articles)

# @admin.register(Payment)
# class PaymentModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user','amount','razorpay_order_id' , 'razorpay_payment_status', 'razorpay_payment_id','paid']

# @admin.register(OrderPlaced)
# class OrderPlacedModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user','product','quantity', 'customer', 'price', 'ordered_date', 'status','payment']