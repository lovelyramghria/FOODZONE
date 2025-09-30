from django.urls import path
from .views import *

urlpatterns = [
path('', home, name='home'),
path('about/', about, name="about"),
path('service/', service, name="service"),
path('food/', food, name="food"),
path('login/',login,name="login"),
path('logout/',logoutuser,name='logout'),
path('register/',register,name="register"),
path('cart/',cart,name="cart"),
path('add_to_cart/<int:food_id>/',add_to_cart,name="add_to_cart"),
path('search/', product_query, name='product_query'),
path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name="remove_from_cart"),
path('pay_now/',pay_now,name='pay_now'),
path('create-checkout-session/',create_checkout_session,name="create-checkout-session"),
path('cake/',cake,name='cake'),
path('snaks/',snaks,name='snaks'),
path('receipes/',receipes,name="receipes"),
path('delete-receipe/<id>/', delete_receipe,name="delete_receipe"),
path('update-receipe/<id>/', update_receipe,name="update_receipe")
 
]