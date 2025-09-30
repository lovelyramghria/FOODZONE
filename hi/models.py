from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Food(models.Model):
    image=models.FileField(upload_to='food',blank=True,null=True,default=True)
    name=models.CharField( max_length=200,blank=True, null=True)
    category = models.ForeignKey(Category, related_name='food', on_delete= models.CASCADE,default=False,null=True)
    description= models.TextField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
      return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='foods', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.food.name} in Cart {self.cart.user.username}"
 
class Services(models.Model):
    image1=models.FileField(blank=True,null=True,default=True)
    name= models.CharField(max_length= 200,null=True)
    description=models.TextField(null=True)
    href=models.CharField(max_length=200,null=True)
   
    def __str__(self):
        return self.name

class Recipe(models.Model):
    receipe_name=models.CharField(max_length=100)
    receipe_description=models.TextField()
    receipe_image=models.FileField(upload_to="receipe")

class C_oder(models.Model):
    image=models.FileField(blank=True,null=True,default=True)
    name=models.CharField(max_length=200,null=True)
    about=models.TextField(null=True)
    price=models.IntegerField(max_length=50)
    href=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class S_oder(models.Model):
    image=models.FileField(blank=True,null=True,default=True)
    name=models.CharField(max_length=100,null=True)
    about=models.TextField(null=True)
    price=models.IntegerField(max_length=20)
    href=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name
    