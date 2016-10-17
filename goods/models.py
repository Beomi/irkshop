from django.db import models

from datetime import date


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Goods(TimeStampModel):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField()
    weight = models.FloatField()
    size = models.FloatField()
    sell_until = models.DateTimeField(blank=True)
    is_valid = models.BooleanField(default=True)

    @property
    def is_available(self):
        if (date.today() < self.sell_until) and self.is_valid:
            return True
        else:
            return False

    def __str__(self):
        if self.is_available:
            status = "구입가능"
        else:
            status = "구입불가"
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
