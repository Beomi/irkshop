from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Goods
from .models import Shipping

from carton.cart import Cart


def index(request):
    return render(request, 'goods/index.html')

def add_cart(request):
    cart = Cart(request.session)
    goods = Goods.objects.get(id=request.GET.get('goods_id'))
    cart.add(goods, price=goods.price)
    return JsonResponse("Added")

def show_cart(request):
    return render(request, 'shopping/show-cart.html')
