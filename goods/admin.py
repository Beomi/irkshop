from django.contrib import admin

from .models import Goods
from .models import GoodsImage
from .models import Category
from .models import Order
from .models import OrderDetail

from core.export_csv import export_as_csv_action


class GoodsImageInline(admin.TabularInline):
    model = GoodsImage
    extra = 0


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    inlines = [GoodsImageInline, ]
    list_display = ['id', 'category', 'name', 'price', 'is_valid', 'is_available', 'current_stock', 'max_stock']
    list_display_links = ['id', 'name']
    list_filter = ['category', 'is_valid']
    list_editable = ['is_valid']
    search_fields = ['name']
    ordering = ['category', 'display_order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'created_at', 'is_paid',
        'address', 'additional_address', 'custom_order',
        'order_detail', 'get_orderdetail_for_this_order',
    )
    actions = [export_as_csv_action("CSV Export")]


admin.site.register(Category)
admin.site.register(OrderDetail)