# Django
from django.db import models
from django.conf import settings
from django.utils.html import format_html
# Python
from datetime import date
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
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Goods(TimeStampModel):
    category = models.ForeignKey(Category, null=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    description = RichTextField()
    weight = models.DecimalField(decimal_places=2, max_digits=10)
    size = models.DecimalField(decimal_places=2, max_digits=10)
    sell_until = models.DateField(null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    @property
    def is_available(self):
        try:
            if ((date.today() <= self.sell_until) or (self.sell_until==None)) and self.is_valid:
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
    goods = models.ForeignKey(Goods, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return self.image.name


class Shipping(TimeStampModel):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    receive_at = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return "({}){}: {} ({})".format(
            self.name,
            self.receive_at,
            self.price,
            self.country
        )


class Order(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_paid = models.BooleanField(default=False)
    address = AddressField(blank=True, null=True)
    additional_address = models.TextField(blank=True, null=True)
    custom_order = models.TextField(blank=True, null=True)

    @property
    def total_price(self):
        total = 0
        order_details = self.orderdetail.all()
        for order in order_details:
            total += order.order_price
        return total

    @property
    def get_orderdetail_for_this_order(self):
        order_details = self.orderdetail.all()
        details = {}
        for detail in order_details:
            details[detail.good.name] = detail.count
        return details


    @property
    def order_detail(self):
        html = ""
        order_details = self.orderdetail.all()
        for detail in order_details:
            html += "<span>{} x {}</span>\n".format(detail.good.__str__(), detail.count)
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
    order = models.ForeignKey(Order, related_name='orderdetail')
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