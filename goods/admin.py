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
    list_display = ['id', 'category', 'name', 'price', 'is_valid', 'is_available', 'current_stock', 'max_stock',
                    'display_order']
    list_display_links = ['id', 'name']
    list_filter = ['category', 'is_valid']
    list_editable = ['is_valid', 'display_order']
    search_fields = ['name']
    ordering = ['category', 'display_order']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'payment_method', 'is_paid', 'created_at',
        'address', 'additional_address', 'custom_order',
        'get_orderdetail_for_this_order_admin'
    )
    actions = [export_as_csv_action("CSV Export")]
    list_select_related = ['user']

    def get_queryset(self, request):
        my_model = super(OrderAdmin, self).get_queryset(request)
        my_model = my_model.prefetch_related('orderdetail_set')
        return my_model

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_order']
    list_editable = ['display_order']


admin.site.register(OrderDetail)
