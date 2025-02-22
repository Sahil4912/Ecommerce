from django.contrib import admin
from .models import Order, Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','pname','offer_price','price']
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
