from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from ..models import *
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import SignUpForm, activate_user
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
import json
from django.utils import timezone
import html
import time
from django.contrib import messages

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = "/login"
    template_name = 'registration/signup.html'
    
    
class ActivateView(TemplateView):
    template_name = "registration/activate.html"
    def get(self, request, uidb64, token, *args, **kwargs):
        result = activate_user(uidb64, token)
        return super().get(request, result=result, **kwargs)

def sent_email(request):
    template_name = "registration/sent_email.html"
    return render(request, template_name)


def mypage(request):
    template_name = "mypage/mypage.html"
    username = User.objects.filter(id=request.user.id).first().username
    follow = Follow.objects.filter(from_user__id=request.user.id).count()
    follower = Follow.objects.filter(to_user__id=request.user.id).count()
    point = Point.objects.filter(user=request.user.id).first().point

    params = {
            "username": username,
            "follow": follow,
            "follower": follower,
            "point": point,
    }
    return render(request, template_name, params)


def profile_update(request):
    user = User.objects.filter(id=request.user.id).first()
    if request.method == 'GET':
        template_name = "mypage/update.html"
        params = {
                "username" : user.username
        }
        return render(request, template_name, params)

    else:
        username = request.POST.get('username')
        if username:
            user.username = username
            user.save()
        return redirect("mypage")


def address(request):
    template_name = "mypage/address.html"
    address_data = Address.objects.filter(user__id=request.user.id)
    params = {
            "address_data": address_data
     }
    return render(request, template_name, params)


def address_create(request):
    template_name = "mypage/change.html"
    return render(request, template_name)


def address_edit(request, address_id):
    address = Address.objects.filter(user__id=request.user.id, id=address_id).first()
    if request.method == 'GET':
        template_name = "mypage/change.html"
        print (address)
        params = {
            "address": address,
        }
        return render(request, template_name, params)
    else:
        lastname = request.POST.get('lastname')
        lastname_furi = request.POST.get('lastname_furi')
        firstname = request.POST.get('firstname')
        firstname_furi = request.POST.get('firstname_furi')
        tel = request.POST.get('tel')
        portalcode = request.POST.get('portalcode')
        prefecture = request.POST.get('prefecture')
        detail1 = request.POST.get('detail1')
        detail2 = request.POST.get('detail2')
        detail3 = request.POST.get('detail3')
        print (lastname, lastname_furi, firstname, firstname_furi, tel, portalcode, prefecture, detail1, detail2, detail3)
        if lastname and lastname_furi and firstname and firstname_furi and tel and portalcode and prefecture and detail1 and detail2:
            address.lastname = lastname
            address.lastname_furi = lastname_furi
            address.firstname = firstname
            address.firstname_furi = firstname_furi
            address.tel = tel
            address.portalcode = int(portalcode)
            address.prefecture = Prefectures(id=prefecture)
            address.detail1 = detail1
            address.detail2 = detail2
            address.detail3 = detail3
            address.save()
            return redirect("address")
        else:
            messages.error(request, "入力内容にエラーがあります")
            return redirect("address_edit", address_id)
