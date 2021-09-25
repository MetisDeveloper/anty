from ..models import *
from django.shortcuts import render, redirect

def home(request):
    if request.method == 'GET':
        template_name = "main/home.html"
        return render(request, template_name)

