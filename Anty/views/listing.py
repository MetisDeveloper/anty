from django.db.models.query_utils import select_related_descend
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
from ..models import *
from django.shortcuts import render, redirect
import time
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from ..util import media
import os

def select_category(request):
    template_name = "listing/select_category.html"
    brand = Brand.objects.all()
    gender = Gender.objects.all()
    category = Category.objects.all()
    params = {
        "brand_list": brand,
        "gender_list": gender,
        "category_list": category,
        }
    return render(request, template_name, params)


def select_temp(request):
    template_name = "listing/select_temp.html"
    brand = request.GET['brand']
    gender = request.GET['gender']
    category = request.GET['category']
    print (brand, gender, category)
    temp_product = Temp_used_product.objects.filter(brand=brand, gender=gender, category=category)
    params = {
            "temp_product_list": temp_product,
            "brand": brand,
            }
    return render(request, template_name, params)




def listing_detail(request):
    if request.method == "GET":
        template_name = "listing/detail.html"
        temp_product = request.GET["temp_id"]
        temp_product = Temp_used_product.objects.filter(id=temp_product).first()
        # 住所変更できるように要改修
        address = Address.objects.filter(user__id=request.user.id).first()
        sche_shipping_date = Sche_sipping_date.objects.all()
        product_status = Product_status.objects.all()
        hope_sell = Hope_sell.objects.all()
        print (sche_shipping_date)

        params = {
            "temp_product": temp_product,
            "address": address,
            "sche_shipping_date_list": sche_shipping_date,
            "product_status_list": product_status,
            "hope_sell_list": hope_sell,
                }
        return render(request, template_name, params)
    else:
        template_name = "listing/comfirm.html"
        fs = FileSystemStorage()
        images = []
        for count in range(1, 6):
            image = request.FILES.get(str("image_"+str(count)))
            if image:
                image = request.FILES[str("image_"+str(count))]
                ext = image.name.split(".")[-1]
                file_name = fs.save(("temporary_image/"+str(request.user.id)+"_"+str(time.time())+"."+ext), image)
                print (file_name)
                media.uploadObject(file_name, os.path.join("/Anty/main/media/",file_name), "/service/image/")
                images.append(file_name)
        temp_product = Temp_used_product.objects.filter(id=request.POST.get("temp_product_id")).first()
        params = {
                "address": Address.objects.filter(user__id=request.user.id).first(),
                "temp_product": temp_product,
                "images": images,
                "selected_sche_sipping_date": Sche_sipping_date.objects.filter(id=request.POST.get('sche_sipping_date')).first(),
                "selected_product_status": Product_status.objects.filter(id=request.POST.get('product_status')).first(),
                "selected_hope_sell": Hope_sell.objects.filter(id=request.POST.get('hope_sell')).first(),
                "price": request.POST.get('price'),
                "detail": request.POST.get('detail'),
                }
        return render(request, template_name, params)


def listing(request):
    template_name = "listing/complete.html"
    if request.method == "POST":
        listing_data = Used_product(
            temp_product = Temp_used_product(id=int(request.POST.get("temp_product"))),
            seller = User(id=request.user.id),
            price = int(request.POST.get("price")),
            explain = request.POST.get("detail"),
            schedule = Sche_sipping_date(id=int(request.POST.get("selected_sche_sipping_date"))),
            status = Product_status(id=int(request.POST.get("selected_product_status"))),
            hope = Hope_sell(id=int(request.POST.get("selected_hope_sell"))),
            is_released = True,
        )
        listing_data.save()

        for count in range(1, 6):
            image = request.POST.get("image"+str(count))
            if image:
                Used_product_image(used_product=Used_product(id=listing_data.id),path=image).save()

        #params = {
        #
        #}
        
        return render(request, template_name)