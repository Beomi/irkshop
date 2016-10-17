from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Goods
from .models import Shipping


@login_required
def index(request):
    return render(request, 'goods/index.html')
