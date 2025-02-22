"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from my_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('about/',views.about),
    path('register/',views.register),
    path('login/',views.ulogin),
    path('logout/',views.ulogout),
    path('product_details/<pid>/',views.product_details),
    path('filterbycategory/<cid>/',views.filterbycategory),
    path('sortbyprice/<sid>/',views.sortbyprice),
    path('pricefilter/',views.pricefilter),
    path('addtocart/<pid>/',views.addtocart),
    path('mycart/',views.viewcart),
    path('removecart/<cid>/',views.removefromcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('address/',views.address),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('order/',views.order),
    path('neworder/',views.neworder),
    path('makepayment/',views.makepayment),
    path('email_send/',views.email_send),
    #path('order_history',views.order_history),
    path('update_order_status',views.update_order_status),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
