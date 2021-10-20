from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from ..models import *
from django.shortcuts import render, redirect
import time
from django.utils import timezone

def used_product_detail(request, used_product_id: int):
    template_name = "purchase/used_product_detail.html"
    product = Used_product.objects.filter(id=used_product_id).first()
    params = {
        "product": product,
    }
    return render(request, template_name, params)


