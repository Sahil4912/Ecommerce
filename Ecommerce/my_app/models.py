from django.db import models

# Create your models here.
class Product(models.Model):
    CAT=((1,"shoes"),(2,"mobile"),(3,"cloths"),(4,"watch"))
    pname=models.CharField(max_length=50,verbose_name="Product name")
    price=models.FloatField()
    category=models.IntegerField(choices=CAT, verbose_name="Category")
    description=models.CharField(max_length=300, verbose_name="details")
    is_active=models.BooleanField(default=True, verbose_name="Is_Avaliable")
    pimage=models.ImageField(upload_to="image")
    offer_price=models.IntegerField(default=0)


    def __str__(self):
        return self.pname

class Cart(models.Model):
    userid=models.ForeignKey('auth.user',on_delete=models.CASCADE,db_column="user_id")
    pid=models.ForeignKey('Product',on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    user_id=models.ForeignKey("auth.User",on_delete=models. CASCADE, db_column="user_id")
    p_id=models.ForeignKey("Product",on_delete=models.CASCADE,db_column="p_id")
    qty=models.IntegerField(default=1)
    amt=models.FloatField()
    payment_status=models.CharField(max_length=20,default='unpaid')

    def _str_(self):
        return self.order_id    
    

class Address(models.Model):
    user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
    address=models.CharField(max_length=100)
    fullname=models.CharField(max_length=40)
    city=models.CharField(max_length=30)
    pincode=models.CharField(max_length=10)
    state=models.CharField(max_length=30)
    mobile=models.CharField(max_length=10)

# class History(models.Model):
#     user_id=models.ForeignKey("auth.User",on_delete=models.CASCADE,db_column="user_id")
#     order_id=models.ForeignKey('Order',on_delete=models.CASCADE,db_column="order_id")
#     amount=models.FloatField()
#     address=models.CharField(max_length=300)
#     status=models.CharField(max_length=30)
     