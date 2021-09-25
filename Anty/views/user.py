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
