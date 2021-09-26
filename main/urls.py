from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from Anty.views import main, user

urlpatterns = [
    path('',login_required(main.home), name="home"),
    path('', include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("signup/", user.SignUpView.as_view(), name="signup"),
    path("mypage/", login_required(user.mypage), name="mypage"),
    path("profile_update/", login_required(user.profile_update), name="profile_update"),
    path("adress/", login_required(user.address), name="address"),
    path("address_create/", login_required(user.address_create), name="address_create"),
    path("address_edit/<int:address_id>/", login_required(user.address_edit), name="address_edit"),
]
