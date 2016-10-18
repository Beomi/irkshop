from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Goods
from .models import Shipping
from .models import Category

from carton.cart import Cart


def index(request):
    categories = Category.objects.all()
    categories_list = []
    for i in categories:
        categories_list.append(i.name)
    goods = Goods.objects.all()
    return render(request, 'goods/index.html', {
        'goods': goods,
        'categories': categories,
        'categories_list': categories_list
    })

def add_cart(request):
    cart = Cart(request.session)
    goods = Goods.objects.get(id=request.GET.get('id'))
    cart.add(goods, price=goods.price)
    return JsonResponse("Added")

def show_cart(request):
    return render(request, 'shopping/show-cart.html')

def remove_cart(request):
    cart = Cart(request.session)
    goods = Goods.objects.get(id=request.GET.get('id'))
    cart.remove(goods)
    return JsonResponse("Removed")
