from django.shortcuts import render
from django.http import JsonResponse

from .models import Goods
from .models import Shipping


def index(request):

    return render(request, 'goods/index.html')
