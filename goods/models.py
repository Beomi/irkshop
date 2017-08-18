# Django
from django.db import models
from django.conf import settings
from django.utils.html import format_html
# Python
from datetime import date
import json
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

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Goods(TimeStampModel):
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = verbose_name

    category = models.ForeignKey(Category, null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = RichTextField()
    sell_until = models.DateField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    @property
    def is_available(self):
        try:
            if ((date.today() <= self.sell_until) or (self.sell_until == None)) and self.is_valid:
                return True
            else:
                return False
        except TypeError:
            if self.is_valid:
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
