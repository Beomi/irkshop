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
    actions = [export_as_csv_action("CSV Export")]


admin.site.register(Category)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Shipping)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail)