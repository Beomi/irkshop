from django.contrib import admin

from .models import Goods
from .models import Shipping


class GoodsImageInline(admin.TabularInline):
    model = Goods
    extra = 3


class GoodsAdmin(admin.ModelAdmin):
    inlines = [GoodsImageInline, ]



admin.site.register(Goods)
admin.site.register(Shipping)