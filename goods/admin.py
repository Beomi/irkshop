from django.contrib import admin

from .models import Goods
from .models import GoodsImage
from .models import Category
from .models import Shipping


class GoodsImageInline(admin.TabularInline):
    model = GoodsImage
    extra = 3


class GoodsAdmin(admin.ModelAdmin):
    inlines = [GoodsImageInline, ]


admin.site.register(Category)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Shipping)