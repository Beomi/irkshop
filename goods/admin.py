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


class GoodsAdmin(admin.ModelAdmin):
    inlines = [GoodsImageInline, ]


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'created_at', 'is_paid',
        'address', 'additioinal_address', 'custom_order',
        'get_orderdetail_for_this_order',
    )
    actions = [export_as_csv_action("CSV Export")]


admin.site.register(Category)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Shipping)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)