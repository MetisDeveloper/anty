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
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    address = Address.objects.filter(user__id=request.user.id).first()
    params = {
            "address": address
     }
    return render(request, template_name, params)


def address_create(request):
    template_name = "mypage/change.html"
    return render(request, template_name)


def address_edit(request):
    address = Address.objects.filter(user__id=request.user.id).first()
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
        postalcode = request.POST.get('postalcode')
        prefecture = request.POST.get('prefecture')
        detail1 = request.POST.get('detail1')
        detail2 = request.POST.get('detail2')
        detail3 = request.POST.get('detail3')
        detail4 = request.POST.get('detail4')
        kana1 = request.POST.get('kana1')
        kana2 = request.POST.get('kana2')
        kana3 = request.POST.get('kana3')
        kana4 = request.POST.get('kana4')
        if lastname and lastname_furi and firstname and firstname_furi and tel and postalcode and prefecture and detail1 and detail2:
            if not address:
                address = Address(user=request.user)
            address.lastname = lastname
            address.lastname_furi = lastname_furi
            address.firstname = firstname
            address.firstname_furi = firstname_furi
            address.tel = tel
            address.postalcode = int(postalcode)
            address.prefecture = Prefectures(id=prefecture)
            address.detail1 = detail1
            address.detail2 = detail2
            address.detail3 = detail3
            address.detail4 = detail4
            address.kana1 = kana1
            address.kana2 = kana2
            address.kana3 = kana3
            address.kana4 = kana4
            
            address.save()
            stripe_id = User.objects.filter(id=request.user.id).first().stripe_id
            account = stripe.Account.retrieve(stripe_id)
            res = stripe.Account.modify(
            stripe_id,
            individual ={
                'first_name':lastname,
                'last_name':firstname,
                'first_name_kana':lastname_furi,
                'last_name_kana':firstname_furi,
                'first_name_kanji':lastname,
                'last_name_kanji':firstname,
                'phone':"+81"+tel,
                # 'gender':"male", #male or female
                'address_kanji':{
                    "country":"JP",
                    "state":Prefectures.objects.filter(id=prefecture).first().name,
                    "city":detail1,
                    "town":detail2,
                    "line1":detail3,
                    "line2":detail4,
                    "postal_code":str(postalcode),
                },
                'address_kana':{
                    "country": "JP", # 2-letter country code
                    "postal_code": str(postalcode), # Zip/Postal Code
                    #"state": , # Prefecture
                    "city": kana1, # City/Ward
                    "town": kana2, # Town/cho-me
                    "line1": kana3, # Block/Building number
                    "line2": kana4, # Building details (optional)
                },
                #'dob':{
                #    "day":"01",
                #    "month":"01",
                #    "year":"1900"
                #},

            },
            business_profile={
                "mcc": "5691",
                "product_description": "古着の出品",
                "url": "https://anty-fashion.jp"
            })
            print (res)
            return redirect("address")
        else:
            messages.error(request, "入力内容にエラーがあります")
            return redirect("address_edit")


def update_emailpass(request):
    template_name = "mypage/mailpass.html"
    params = {
        "email": User.objects.filter(id=request.user.id).first().email,
    }
    return render(request, template_name, params)


def new_email(request):
    if request.method == 'GET':
        template_name = "mypage/newmail.html"
        return render(request, template_name)
    else:
        email = request.POST.get("email")
        if email:
            user = User.objects.filter(id=request.user.id).first()
            user.email = email
            user.save()
            res = stripe.Account.modify(
            user.stripe_id,
            individual ={
                "email": email,
            },
            )
            print (res)
        return redirect("update_emailpass")