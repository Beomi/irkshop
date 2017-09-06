from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls.base import reverse_lazy, reverse

from .models import Goods
from .models import Category
from .models import Order
from .models import OrderDetail
from .forms import OrderForm
# from .tasks import check_payment

from carton.cart import Cart
from django.contrib.auth.models import User

from core.send_mail import send_mail, send_gmail

from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

import csv
from datetime import datetime
import requests
import json


def index(request):
    categories = Category.objects.all()
    categories_list = []
    for i in categories:
        categories_list.append('SHOP' + i.name)
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
                'message': "Added {}".format(goods.name)
            })
    return JsonResponse({
        'message': "Please Access with AJAX/POST"
    })


def update_cart(request):
    if request.method == 'POST':
        if request.is_ajax():
            cart = Cart(request.session)
            quantity = request.POST.get('quantity')
            goods = Goods.objects.get(id=request.POST.get('good'))
            cart.set_quantity(goods, quantity)
            return JsonResponse({
                'message': 'update {} for {}'.format(
                    goods.name, quantity
                ),
                'total': cart.total,
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
def payment(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form.errors)
        if form.is_valid():
            this_order = form.save(commit=False)
            cart = Cart(request.session).cart_serializable
            payment_method = request.POST['payment-method']
            this_order.user = request.user
            this_order.save()
            order_number = this_order.pk
            for v in cart.values():
                order_detail = OrderDetail()
                order_detail.good = Goods.objects.get(pk=v['product_pk'])
                order_detail.count = v['quantity']
                order_detail.order = this_order
                order_detail.save()

            if payment_method == 'paypal':
                # paypal
                this_order = Order.objects.get(pk=order_number)

                total_price = this_order.total_price
                if len(this_order.orderdetail_set.all()) > 1:
                    item_name = this_order.orderdetail_set.all()[0].good.name \
                                + this_order.orderdetail_set.all()[1].good.name + '...'
                else:
                    item_name = this_order.orderdetail_set.all()[0].good.name

                paypal_dict = {
                    "business": "{}".format(settings.PAYPAL_ID),
                    "amount": "{}".format(total_price),
                    "item_name": item_name,
                    "invoice": "{}".format(this_order.uuid),
                    "notify_url": settings.PAYPAL_URL + reverse('paypal-ipn'),
                    "return_url": settings.PAYPAL_URL + '/shop/thankyou/' + str(this_order.uuid),
                    "cancel_return": settings.PAYPAL_URL + reverse('index'),
                    "custom": "{}".format(this_order.user)
                }
                paypal_form = PayPalPaymentsForm(initial=paypal_dict).render()
                send_gmail(
                    send_to=str(this_order.user.email),
                    subject='IRKSHOP: Thankyou for your Order!',
                    order=this_order
                )
                # clear cart
                Cart(request.session).clear()
                return JsonResponse({
                    'message': "Sucessfully Ordered!\n"
                               "We've send you your order mail.\n"
                               "Please Continue with Paypal Payment.\n"
                               "(Paypal Checkout will show soon.)",
                    'paypal-form': paypal_form
                })
            elif payment_method == 'bank-transfer':
                send_gmail(
                    send_to=str(this_order.user.email),
                    subject='IRKSHOP: Please Proceed Bank Transfer to finish your purchase',
                    order=this_order
                )
                # clear cart
                Cart(request.session).clear()
                return JsonResponse({
                    'message': "Sucessfully Ordered!\n"
                               "Please Continue with Bank Transfer.\n"
                               "We've mailed you our invoice.",
                    'redirect': '/shop/thankyou/' + str(this_order.uuid)
                })
        else:
            return JsonResponse({
                'message': 'Order Form is not fully filled!\n'
                           'NOTE: Ingress Email and Agent Name are Required'
            })
    else:
        form = OrderForm()

    return render(request, 'payment/payment.html', {
        'form': form,
    })


@login_required
def get_my_order(request):
    my_orders = Order.objects.filter(user=request.user).prefetch_related('orderdetail_set')
    return render(request, 'my_orders.html', {
        'my_orders': my_orders
    })


# Paypal Payment Checking
@csrf_exempt
def check_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.receiver_email != settings.PAYPAL_ID:
            return False
        try:
            order = Order.objects.get(uuid=ipn_obj.invoice)
            if ipn_obj.mc_gross == order.total_price:
                order.is_paid = True
                order.save()
                user = order.user
                send_mail(
                    user=settings.GMAIL_ID,
                    pwd=settings.GMAIL_PW,
                    recipient=user.email,
                    subject="Payment to IRKSHOP",
                    body="Hello {},\n"
                         "We've Just got your PAYMENT from PAYPAL.\n"
                         "This is the confirm of your Order's payment.\n"
                         "Your Order Invoice Number: #{}\n"
                         "Total Payment Amount: ${}\n"
                         "Thanks again for your Order.\n"
                         "Sincerely, IRK.".format(
                        user,
                        order.pk,
                        ipn_obj.mc_gross
                    ),
                )
                return True
        except:
            return False


@csrf_exempt
def cancel_payment(request):
    pass


@csrf_exempt
def thank_you(request, order_uuid):
    order = Order.objects.get(uuid=order_uuid)
    return render(request, 'mail_template.html', {
        'order': order
    })


valid_ipn_received.connect(check_payment)


# Staff Order View Page
@staff_member_required
def orderlist(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; ' \
                                      'filename="IRKSHOP_ORDERLIST_{}.csv"'.format(
        datetime.now().strftime("%Y%m%d%H%M")
    )

    writer = csv.writer(response)
    writer.writerow(
        ['Invoice Number', 'User Email', 'Pay Amount', 'Order Details', 'Custom Orders', 'Shipping Address'])

    qs = Order.objects.filter(is_paid=True).prefetch_related('orderdetail_set')

    for order in qs:
        details = order.orderdetail_set.all()

        order_details = {}
        try:
            for i in details:
                order_details[i.good.name] = i.count
        except TypeError:
            order_details[details.good.name] = details.count

        if order.address != None:
            address = order.address.__str__() + ' // ' + order.additional_address
        else:
            address = ''

        writer.writerow([order.pk, order.user.email, order.total_price, order_details, order.custom_order, address])

    return response


# Korea Bank Check
def korea_bank_payment(request, order_number):
    order = Order.objects.get(pk=order_number)
    currency = requests.get('http://www.floatrates.com/daily/usd.json')
    today_usd_to_krw = int(json.loads(currency)['krw']['rate'] / 10) * 10  # NOT to get 1won but 10won
    if request.method == 'POST':
        pass
    else:
        if order.is_paid:
            return JsonResponse({
                'message': 'This transaction is already paid!'
            })
        data = {
            "amount": order.total_price * today_usd_to_krw,
            "order_number": order_number,
            "today_usd_to_krw": today_usd_to_krw
        }

        return render(request, 'payment/korea_bank_payment.html', data)
