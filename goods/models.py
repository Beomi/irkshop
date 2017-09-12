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

    def get_available_goods(self):
        return [x for x in self.goods_set.all() if x.is_available is True]


class Goods(TimeStampModel):
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = verbose_name
        ordering = ['category', 'display_order']

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
            if ((date.today() <= self.sell_until) or (self.sell_until == None)) \
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

    PAYMENT_METHODS = (
        ('b', '계좌이체'),
        ('p', 'Paypal'),
    )

    HOW_TO_RECEIVE_KRW = (
        ('f', '현장수령'),
        ('l', '뒷풀이수령'),
        ('s', '배송(한국)')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='주문고객')
    is_paid = models.BooleanField('결제완료', default=False)
    is_shipping = models.BooleanField('배송건', default=False)
    address = AddressField(verbose_name='주소', blank=True, null=True)
    additional_address = models.TextField('상세주소', blank=True, null=True)
    custom_order = models.TextField('주문요청건', blank=True, null=True)
    ingress_mail = models.EmailField('Ingress 메일주소', blank=True)
    ingress_agent_name = models.CharField('Ingress Agent Name', max_length=200)
    payment_method = models.CharField('결제수단', max_length=1, choices=PAYMENT_METHODS, default='b')
    usd_to_krw = models.IntegerField('환율', default=0)
    bank_transfer_name = models.CharField('계좌이체 표시이름', max_length=20, default='')
    how_to_receive_krw = models.CharField('(한국)수령방법', max_length=1, choices=HOW_TO_RECEIVE_KRW, blank=True, null=True)

    @property
    def total_price(self):
        total = 0
        order_details = self.orderdetail_set.all()
        for od in order_details:
            total += od.order_price
        if self.is_shipping:
            # TODO: Let use this not FIXED
            total += 35
        return total

    @property
    def total_price_krw(self):
        total = 0
        order_details = self.orderdetail_set.all()
        for od in order_details:
            total += od.order_price_krw
        if self.is_shipping:
            # TODO: Let use this not FIXED
            total += 5000
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
    def get_orderdetail_for_this_order_admin(self):
        order_details = self.orderdetail_set.all()
        details = ""
        for detail in order_details:
            details += "{} (x{})\n".format(detail.good.name, detail.count)
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

    @property
    def order_price_krw(self):
        return self.good.price * self.count * self.order.usd_to_krw

    def __str__(self):
        if self.order_price_krw:
            return '#{} / {}원'.format(
                self.order.pk,
                self.order_price_krw
            )
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
