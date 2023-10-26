from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from .models import *
from django.db.models import Count
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
import json

def home(request):
    return render(request, 'Home.html' )

def checkout(request):
    return render(request, 'checkout.html' )

def contact(request):
    return render(request, 'contact.html' )

def about(request):
    return render(request, 'about.html' )

def event(request):
    return render(request, 'Event.html' )


# LOGIN / SIGNUP

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'login.html',context )

def logout(request):
    auth.logout(request)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    context = {'form':form}
    return render(request, 'signup.html',context )

def contact (request):
    if request.method == "POST":
        name_contact = request.POST["name"]
        subject_contact = request.POST["subject"]
        email_contact = request.POST["email"]
        message_contact = request.POST["message"]

        Contact(contact_name=name_contact, contact_subject=subject_contact, 
        contact_email = email_contact, contact_message=message_contact).save()
        
    return render(request, 'contact.html')

def products(request):
    products = Product.objects.all()
    context ={"products":products}
    return render(request, 'products.html',context )

def Product_Detail(request, id):
    products = Product.objects.get(product_id=id)
    context ={"products":products}
    return render(request, 'Product_Detail.html', context )

# Shtimi ne cart e produktit + ruajtja nd DB
def add_to_cart(request, pk):
    if request.user.is_authenticated:
        # pk - primary key by default (e perzgjedh vete)
        item = get_object_or_404(Product, pk=pk) # merr produktin ne eshte perndryshe shfaq sms qe nukeshte
        # Merr ose krijon produktin ne varesi te user
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        # Filtron porosine e user
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists(): # nese porosia e user ekziston 
            order = order_qs[0]  # merr porosine e pare
            if order.orderitems.filter(item=item).exists(): # ben kontrollin nese produkti eshte porositur
                order_item[0].quantity += 1 # rrit sasine e produktit
                order_item[0].save() # ruan produktin
                messages.info(request, "This item quantity was updated!")
                return redirect('cart')
            else:
                order.orderitems.add(order_item[0]) #nese nuk eshte shtoje
                messages.info(request, "This item was added to your cart!")
                return redirect('cart')
        else:
            order = Order(user=request.user) # nese eshte porosi e re
            order.save() # ruaje
            order.orderitems.add(order_item[0]) #shto produktet
            messages.info(request, "This item was added to your cart!")
            return redirect('cart')
    else:
        return redirect('login')

# Shfaqja e cart
def cart(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts': carts,
            'order': order
        }
        return render(request, 'cart.html', context)
    else:
        messages.warning(request, "You don't have any item in your cart!")
        return redirect('home')

def shipInfo(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        context = {
            'carts': carts,
            'order': order
        }
        return render(request, 'checkout1.html', context)

# Heq nje produkt nga cart
def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            order.orderitems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was remove from your cart!")
            return redirect('cart')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('cart')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('cart')

# shton sasine e nje produkti
def increase_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, f"{item.product_title} quantity has been updated")
                return redirect('cart')
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect('cart')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('cart')

# ul sasine e nje produkti
def decrease_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitems.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, f"{item.product_title} quantity has been updated")
                return redirect('cart')
            else:
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, f"{item.product_title} item has been removed from your cart")
                return redirect('cart')
        else:
            messages.info(request, f"{item.product_name} is not in your cart")
            return redirect('cart')
    else:
        messages.info(request, "You don't have an active order")
        return redirect('cart')

def articles(request):
    articles = Articles.objects.all()
    context ={"articles":articles}
    return render(request, 'article.html',context )

def article_Detail(request, id):
    articles = Articles.objects.get(articles_id=id)
    context ={"articles":articles}
    return render(request, 'article_Detail.html', context)




