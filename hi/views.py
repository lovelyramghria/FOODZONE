from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.http import HttpResponseBadRequest
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')
 
def service(request):
    items= Services.objects.all()
    return render(request,"service.html",{"items":items})

def cart(request):
    return render(request,"cart.html")

@login_required(login_url='/login/')
def cake(request):
    cakes=C_oder.objects.all()
    return render(request,"cake.html",{"cakes":cakes})

@login_required(login_url='/login/')
def snaks(request):
    snaks=S_oder.objects.all()
    return render (request,"snaks.html",{"snaks":snaks})

def login(request):
    if request.method== "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            return redirect ("login")
    else:
         return render(request,"login.html")

def logoutuser(request):
    logout(request)
    return redirect('login')


def register(request):
   if request.method == "POST":
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      password = request.POST.get('password')
         
      user = User.objects.filter(username=username)
      if user.exists():
          messages.info(request, "username already exists")
          return redirect('/register/')
      user = User.objects.create(
      first_name = first_name,
      last_name = last_name,
      username = username,
       )   
      user.set_password(password)
      user.save()
      messages.info(request, "user created successfully")
      return redirect('/register/')
   return render(request,'register.html')

 
def food(request):
    categories=Category.objects.all()
    food= Food.objects.all()
    return render(request,"food.html",{'categories': categories ,'food':food})

def product_query(request):
    if not request.user.is_authenticated:
        return redirect('login')
    query = request.GET.get('q', '')
    if query:
        categories = Category.objects.filter(food__name__icontains=query).distinct()
    else:
        categories = Category.objects.all()
    return render(request, 'food.html', {'categories': categories, 'query': query})

@login_required(login_url='/login/')
def cart(request):
    cart,created =Cart.objects.get_or_create(user=request.user)
    cart_items = cart.foods.all()  # Get CartItems related to the current Cart
    total_price = sum(cart_item.quantity * cart_item.food.price for cart_item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'cart': cart})

@login_required(login_url='/login/')
def add_to_cart(request, food_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    food= Food.objects.get(id=food_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{food.name} Added in your cart.")
    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    food_name = cart_item.food.name
    cart_item.delete()
    messages.success(request, f"{food_name} removed from your cart.")
    return redirect('cart')

def receipes(request):
    if request.method=="POST":
     data=request.POST
     receipe_image = request.FILES.get('recepie_image')
     receipe_name =data.get('receipe_name')
     receipe_description = data.get('receipe_description')

     Recipe.objects.create(
        receipe_image=  receipe_image,
        receipe_name= receipe_name,
        receipe_description =receipe_description
     )
    return render(request,'recepies.html')
def pay_now(request):
    if request.method == 'POST':
        pass
    return render(request, 'checkout.html')

import logging

stripe.api_key = "sk_test_51QeX9T09Rphq45Gj2vnRAxhqG0cZjxgOtKgYBLLPvHqLgBSspusm5ddYcBhJ3jaksGB7IKKy1hpXXKdPnR0wrJXD00R1HnD75S"


def create_checkout_session(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created= Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    total_price=0

    for cart_item in cart_items:
        unit_price_in_paise = int(cart_item.food.price * 100)
        item_total_amount = unit_price_in_paise * cart_item.quantity
        total_price += item_total_amount
    print(f"Total price of the cart: {total_price} paise")
    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': total_price, 
                        'product_data': {
                            'name': "Cart Total",  
                        },
                    },
                    'quantity': 1, 
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return HttpResponseBadRequest(f"Error creating checkout session: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method.")
 
def receipes(request):
   if request.method == "POST":
     data=request.POST
     
     receipe_image = request.FILES.get('recepie_image')
     receipe_name = data.get('receipe_name')
     receipe_description = data.get('receipe_description')

     Recipe.objects.create(
        receipe_image =  receipe_image,
        receipe_name = receipe_name,
        receipe_description = receipe_description,
        )
     return redirect('/receipes/')
   queryset = Recipe.objects.all()
   context = {'receipe':queryset}
   return render(request,'recepies.html',context)


def update_receipe(request,id):
   queryset = Recipe.objects.get(id = id)

   if request.method =="POST":
     data=request.POST
     receipe_image = request.FILES.get('recepie_image')
     receipe_name = data.get('receipe_name')
     receipe_description = data.get('receipe_description')

     queryset.receipe_name = receipe_name
     queryset.receipe_description = receipe_description

     if receipe_image:
        queryset.receipe_image = receipe_image

     queryset.save()
     return redirect('/receipes/')

   context = {'receipe':queryset}
   return render(request,'update_receipes.html',context)

def delete_receipe(request,id):
   queryset = Recipe.objects.get(id=id)
   queryset.delete()
   return redirect('/receipes/')

 
 
