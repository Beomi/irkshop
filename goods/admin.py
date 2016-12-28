from django.contrib import admin

from .models import Goods
from .models import GoodsImage
from .models import Category
from .models import Shipping
from .models import Order
from .models import OrderDetail

from core.export_csv import export_as_csv_action


class GoodsImageInline(admin.TabularInline):
    model = GoodsImage
    extra = 3


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    inlines = [GoodsImageInline, ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'created_at', 'is_paid',
        'address', 'additional_address', 'custom_order',
        'order_detail',
    )
    actions = [export_as_csv_action("CSV Export")]


admin.site.register(Category)
admin.site.register(Shipping)
admin.site.register(OrderDetail)