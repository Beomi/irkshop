# Django
from django.db import models
from django.conf import settings
from django.utils.html import format_html
# Python
from datetime import date
import json
import uuid
# Pip
from ckeditor.fields import RichTextField
from address.models import AddressField
from carton.cart import Cart


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = verbose_name
        ordering = ['display_order']

    name = models.CharField(max_length=200)
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='카테고리 순서(작은게 먼저)')

    def __str__(self):
        return self.name


class Goods(TimeStampModel):
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = verbose_name
        ordering = ['display_order']

    category = models.ForeignKey(Category, null=True, verbose_name='카테고리')
    display_order = models.PositiveSmallIntegerField(default=0, verbose_name='카테고리 내 순서(작은게 먼저)')
    name = models.CharField(max_length=200, verbose_name='상품명')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격(달러)')
    description = RichTextField(verbose_name='상품설명')
    sell_until = models.DateField(null=True, blank=True, verbose_name='판매종료일')
    is_valid = models.BooleanField(default=True, verbose_name='판매중')
    max_stock = models.PositiveIntegerField(default=1000, verbose_name='판매 재고(전체)')

    def current_stock(self):
        stock = self.max_stock
        for od in OrderDetail.objects.filter(order__is_paid=True):
            if od.good == self:
                stock -= od.count
        return stock

    @property
    def is_available(self):
        try:
            if ((date.today() <= self.sell_until) or (self.sell_until == None))\
                    and self.is_valid \
                    and self.current_stock() > 0:
                return True
            else:
                return False
        except TypeError:
            if self.is_valid and self.current_stock() > 0:
                return True
            else:
                return False

    def __str__(self):
        if self.is_available:
            status = "available"
        else:
            status = "NOT_AVAILABLE"
        return "{}({})".format(
            self.name,
            status
        )

    def get_first_image(self):
        try:
            image = self.images.all()[0]
        except:
            image = ''
        return image


class GoodsImage(TimeStampModel):
    class Meta:
        verbose_name = '상품 이미지'
        verbose_name_plural = verbose_name

    goods = models.ForeignKey(Goods, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return self.image.name


class Order(TimeStampModel):
    class Meta:
        verbose_name = '주문건'
        verbose_name_plural = verbose_name

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_paid = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    address = AddressField(blank=True, null=True)
    additional_address = models.TextField(blank=True, null=True)
    custom_order = models.TextField(blank=True, null=True)
    ingress_mail = models.EmailField(blank=True)
    ingress_agent_name = models.CharField(max_length=200)

    @property
    def total_price(self):
        total = 0
        order_details = self.orderdetail_set.all()
        for order in order_details:
            total += order.order_price
        if self.is_shipping:
            # TODO: Let use this not FIXED
            total += 8
        return total

    @property
    def get_orderdetail_for_this_order(self):
        order_details = self.orderdetail_set.all()
        details = {}
        for detail in order_details:
            details[detail.good.name] = detail.count
        if self.is_shipping:
            details['shipping'] = True
        return details

    def get_orderdetail_email_template(self):
        order_details = self.orderdetail_set.all()
        details = {}
        for detail in order_details:
            details[detail.good.name] = [detail.count, detail.order_price]
        if self.is_shipping:
            details['shipping'] = True
        return details

    @property
    def order_detail(self):
        html = ""
        order_details = self.orderdetail_set.all()
        for detail in order_details:
            html += "<span>{} x {}</span><br>\n".format(detail.good.__str__(), detail.count)
        return format_html(html)

    def __str__(self):
        if self.is_paid:
            paid = '결제완료'
        else:
            paid = '결제대기'
        return '#{} / {} / {} / ${} / 주문내역: {}{}'.format(
            self.pk,
            self.user,
            paid,
            self.total_price,
            self.get_orderdetail_for_this_order,
            self.custom_order
        )


class OrderDetail(TimeStampModel):
    class Meta:
        verbose_name = '주문상세'
        verbose_name_plural = verbose_name

    order = models.ForeignKey(Order)
    good = models.ForeignKey(Goods)
    count = models.PositiveSmallIntegerField()

    @property
    def order_price(self):
        return self.good.price * self.count

    def __str__(self):
        return '#{} / ${}'.format(
            self.order.pk,
            self.order_price
        )


class OrderHistory(TimeStampModel):
    class Meta:
        verbose_name = '주문내역'
        verbose_name_plural = verbose_name

    order = models.OneToOneField('Order')
    history = models.TextField()

    def save_json(self, x):
        self.history = json.dumps(x)

    def load_json(self):
        return json.loads(self.history)
