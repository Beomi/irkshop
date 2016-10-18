from django.db import models

from datetime import date

from ckeditor.fields import RichTextField


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
    price = models.IntegerField()
    description = RichTextField()
    weight = models.FloatField()
    size = models.FloatField()
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
            status = "구입가능"
        else:
            status = "단종"
        return "{}({})".format(
            self.name,
            status
        )


class GoodsImage(TimeStampModel):
    goods = models.ForeignKey(Goods, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return self.image.name


class Shipping(TimeStampModel):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    receive_at = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return "({}){}: {} ({})".format(
            self.name,
            self.receive_at,
            self.price,
            self.country
        )
