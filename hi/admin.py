from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Services)
admin.site.register(C_oder)
admin.site.register(S_oder)
class FoodAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'category','price','image')  # Adjust fields as needed
    search_fields = ('name', 'category__name')
    filter = ('category')
    def food_name(self, obj):
        return obj.name

admin.site.register(Food,FoodAdmin)
admin.site.register(Cart)
admin.site.register(Recipe)

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','created_at',)
    list_filter= ('created_at',)
    search_fields=('user__username',)

admin.site.register(CartItem)

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','cart','quantity','created_at')
    list_filter=( 'created_at',)
    search_fields=('food__name','cart__user__username',)