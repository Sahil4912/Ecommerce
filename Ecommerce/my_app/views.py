from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Address, Order#, History
import re
import random
import razorpay
from django.core.mail import send_mail
# Create your views here.
def index(request):
    context={}
    products=Product.objects.all()
    print(products)
    context['products']=products
    return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')

def register(request):
    context={}
    if request.method=='POST':
        un=request.POST["uname"]
        en=request.POST["ename"]
        up=request.POST["upass"]
        uc=request.POST["ucpass"]
        if un=="" or en=="" or up=="" or uc=="":
            context["error_msg"]="All fields are required please enter all fields"
            return render(request,'register.html',context)
        elif up!=uc:
            context["error_msg"]="Password and confirm password not matched"
            return render(request,'register.html',context)
        elif len(up) < 8:
            context["error_msg"]="Password contain atleast 8 characters"
            return render(request,'register.html',context)
        else:
            u=User.objects.create(username=un,email=en)
            u.set_password(up)
            u.save()
            return redirect('/login') 
    else:
        return render(request,'register.html')
    
def ulogin(request):
    context={}
    if request.method == "POST":
        un=request.POST["uname"]
        ep=request.POST["upass"]
        print(un,ep)
        if un=="" or ep=="":
            context["error_msg"]="All fields are required"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=un,password=ep)
            print(u)
            if u!=None:
                login(request,u)
                return redirect('/')
            else:
                context["error_msg"]="Invalid username and password"
                return render(request,'login.html',context)
            
            
    else:
        return render(request, 'login.html')
    
def ulogout(request):
    logout(request)
    return redirect('/login')

def product_details(request,pid):
    context={}
    prod=Product.objects.filter(id=pid)
    context["product"]=prod
    return render(request,'product.html',context)

def filterbycategory(request,cid):
    context={}
    products=Product.objects.filter(category=cid)
    context['products']=products

    return render(request,'index.html',context)

def sortbyprice(request,sid):
    context={}
    if sid == '0':
        products=Product.objects.order_by('price')
    else:
         products=Product.objects.order_by('-price')

    context["products"]=products
    return render(request,'index.html',context)

def pricefilter(request):
    context={}
    mx=request.GET['max']
    mn=request.GET['min']
    q1=Q(offer_price__gte=mn)
    q2=Q(offer_price__lte=mx)
    products=Product.objects.filter(q1 & q2)
    context['products']=products
    return render(request,'index.html',context)

def addtocart(request,pid):
    product=Product.objects.filter(id=pid)
    context={}
    context['product']=product 
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        print(u[0],p[0])
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        cart=Cart.objects.filter(q1 & q2)
        if len(cart)==1:
            context['error_msg']="Product already in cart!"
            return render(request,'product.html',context)
        else:
         cart=Cart.objects.create(userid=u[0], pid=p[0])
         cart.save()
         context['success']="product added in cart"
         return render(request,'product.html',context)
    
    else:
        context['error_msg']="Please Login First"
        return render(request,'product.html',context)
    
def viewcart(request):
    context={}
    carts=Cart.objects.filter(userid=request.user.id)
    saving_amt=0
    total_amt=0
    actual_amt=0
    for cart in carts:
        saving_amt+=(cart.pid.price - cart.pid.offer_price) * cart.qty
        total_amt+=cart.pid.offer_price * cart.qty
        actual_amt+=cart.pid.price
    print(saving_amt)
    print(total_amt)
    print(actual_amt)
    context['saving']=saving_amt
    context['total']=total_amt
    context['actual']=actual_amt
    context['items']=len(carts) 
    if len(carts)==0:
        context['text']="No items in your cart"
        context['text1']="Continue shopping"
        return render(request,'cart.html',context)
    else:
     context['carts']=carts
     print(carts)
     return render(request,'cart.html',context)
    
def updateqty(request,x,cid):
    cart=Cart.objects.filter(id=cid)
    quantity=cart[0].qty
    print(quantity)
    if x=='1':
        quantity+=1
    elif quantity > 1:
        quantity-=1
    cart.update(qty=quantity)
    return redirect('/mycart')
 
def removefromcart(request,cid):
    cart=Cart.objects.filter(id=cid)
    cart.delete()
    return redirect('/mycart')
    
def order(request):
    return render(request,'myorder.html')

def neworder(request):
    return render(request,'placeorder.html')

def address(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    add=Address.objects.filter(user_id=u[0])
    if len(add)>=1:
        return redirect('/placeorder')
    else:
        if request.method=="POST":
            fn=request.POST["full_name"]
            ad=request.POST["address"]
            ct=request.POST["city"]
            st=request.POST["state"]
            zp=request.POST["zipcode"]
            mob=request.POST["mobile"]
            if re.match('[6-9]\d{9}',mob):
                address=Address.objects.create(user_id=u[0],fullname=fn,address=ad,city=ct,state=st,pincode=zp,mobile=mob)
                address.save()
                return redirect('/placeorder')

            else:
                context['error_msg']="Please enter valid mobile number"
                return render(request,'address.html',context)
        else:
            return render(request, 'address.html')
        

def placeorder(request):
    carts=Cart.objects.filter(userid=request.user.id)
    for i in carts:
        oid=random.randint(1111,9999)
        totalamt=i.pid.offer_price*i.qty
        order=Order.objects.create(order_id=oid,user_id=i.userid,p_id=i.pid,amt=totalamt,qty=i.qty)
        order.save()
    carts.delete()
    return redirect('/fetchorder')


def fetchorder(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    carts=Cart.objects.filter(userid=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)
    address=Address.objects.filter(user_id=u[0])
    context['address']=address


    carts=Cart.objects.filter(userid=request.user.id)
    saving_amt=0
    total_amt=0
    items=0
    # total=0
    # q=0

    # for i in orders:
    #     total+=i.amt
    #     q+=i.qty
    # context=['total']=total
    # context=['item']=q

    for cart in carts:
        saving_amt += (cart.pid.price - cart.pid.offer_price) * cart.qty
        total_amt += cart.pid.offer_price * cart.qty
        items+=cart.qty

        context['saving']=saving_amt
        context['amount']=total_amt
        context['items']=items 

    return render(request, 'placeorder.html',context)

def makepayment(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)

    sum=0
    context['orders'] = orders

    for order in orders:
        sum+=order.amt
        orderid=order.order_id

    client=razorpay.Client(auth=("rzp_test_K8LrQ5HvEUvK5c", "f93z5IHrBk7W8iVO1sEZeHvC"))
    data={"amount":sum*100, "currency": "INR", "receipt": orderid}
    payment=client.order.create(data=data)
    context['payment']=payment
    return render(request,'pay.html',context)


def email_send(request):
    send_mail(
        'Confirmation of order',
        'Your order is confirmed \n Thanks for ordering',
        'sahilpawar2312003@gmail.com',
        ['azadshaikh072@gmail.com']

    )

    return redirect('/update_order_status')


def update_order_status(request):
    context={}
    u=User.objects.filter(id=request.user.id)
    q1=Q(user_id=u[0])
    q2=Q(payment_status="unpaid")
    orders=Order.objects.filter(q1&q2)
    orders.update(payment_status='paid')

    for order in orders:
        order.update(payment_status='paid')

    return redirect('/')


# def order_history(request):
#     user=User.objects.filter(id=request.user.id)
#     orders=Order.objects.filter(user_id=user[0])
#     addr=Address.objects.filter(user_id=user[0])
#     a=''
#     for x in addr:
#         a+=x.fullname+" "+x.address+" "+x.city+" "+x.state+" "+x.pincode
#     print(a)

#     for i in orders:
#         myorder=History.objects.create(user_id=user[0], order_id=orders[0], amount=i.amt,address=a, status="Delivered")
#         myorder.save()

#     return HttpResponse('Your history is created')



