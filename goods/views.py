from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Goods
from .models import Shipping
from .models import Category
from .models import Order
from .models import OrderDetail
from .forms import AddressForm

from carton.cart import Cart

import json


def index(request):
    categories = Category.objects.all()
    categories_list = []
    for i in categories:
        categories_list.append('SHOP'+i.name)
    goods = Goods.objects.all()
    return render(request, 'goods/index.html', {
        'goods': goods,
        'categories': categories,
        'categories_list': categories_list
    })

def add_cart(request):
    if request.method == 'POST':
        if request.is_ajax():
            cart = Cart(request.session)
            goods = Goods.objects.get(id=request.POST.get('good'))
            cart.add(goods, price=goods.price)
            return JsonResponse({
                'message':"Added {}".format(goods.name)
            })
    return JsonResponse({
        'message':"Please Access with AJAX/POST"
    })

def update_cart(request):
    if request.method == 'POST':
        if request.is_ajax():
            cart = Cart(request.session)
            quantity = request.POST.get('quantity')
            goods = Goods.objects.get(id=request.POST.get('good'))
            cart.set_quantity(goods, quantity)
            return JsonResponse({
                'message':'update {} for {}'.format(
                    goods.name, quantity
                )
            })

def show_cart(request):
    cart = Cart(request.session)
    context = {"items": cart.items}
    return render(request, 'shopping/shopping-cart.html', context=context)

def current_cart(request):
    cart = Cart(request.session)
    return JsonResponse(dict(data=cart.items_serializable))

def remove_cart(request):
    if request.method == 'POST':
        if request.is_ajax():
            cart = Cart(request.session)
            goods = Goods.objects.get(pk=request.POST.get('good'))
            cart.remove(goods)
            return JsonResponse({
                'message': "Removed"
            })

def clear_cart(request):
    if request.method == 'POST':
        if request.is_ajax():
            cart = Cart(request.session)
            cart.clear()
            return JsonResponse({
                'message': 'cleared cart'
            })

@login_required
def payment_local(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            this_order = Order()
            cart = Cart(request.session).cart_serializable
            this_order.address = form.address
            this_order.additional_address = request.POST.get('AdditionalAddress')
            this_order.user = request.user
            this_order.save()
            for k, v in cart:
                order_detail = OrderDetail()
                order_detail.good = Goods.objects.get(pk=v.product_pk)
                order_detail.count = v.quantity
                order_detail.order = this_order
            return redirect(reverse(thank_you))
    else:
        form = AddressForm()

    return render(request, 'payment/payment_local.html', {
        'form': form,
    })

def thank_you(request):
    return render(request, 'payment/thankyou.html')