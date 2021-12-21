
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from Anty.views import main, user, line_bot, listing, purchase

urlpatterns = [
    path('',login_required(main.home), name="home"),
    path('', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("signup/", user.SignUpView.as_view(), name="signup"),
    path("mypage/", login_required(user.mypage), name="mypage"),
    path("profile_update/", login_required(user.profile_update), name="profile_update"),
    path("adress/", login_required(user.address), name="address"),
    path("address_create/", login_required(user.address_create), name="address_create"),
    path("address_edit/", login_required(user.address_edit), name="address_edit"),
    path("update_emailpass/", login_required(user.update_emailpass), name="update_emailpass"),
    path("new_email/", login_required(user.new_email), name="new_email"),
    path("line_bot/", line_bot.index, name="line_bot"),
    path("select_category/", login_required(listing.select_category), name="select_category"),
    path("select_temp/", login_required(listing.select_temp), name="select_temp"),
    path("listing_detail/", login_required(listing.listing_detail), name="listing_detail"),
    path("listing/", login_required(listing.listing), name="listing"),
    path("used_product_detail/<int:used_product_id>/", login_required(purchase.used_product_detail), name="used_product_detail"),
]
