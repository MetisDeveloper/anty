from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ipware import get_client_ip
from .models import Point
import time
import stripe

stripe.api_key = "sk_test_51Je5QnLizjvjeOWvoDdzagTaNh0nXvtZ77aOw99qnbFbqvnDuLyYzJRAz3CNop3YTgSCPhweH6ULOLvv9ZSwTwGH00Q8igKXit"

User = get_user_model()


subject = "登録確認"
message_template = """
ご登録ありがとうございます。
以下URLをクリックして登録を完了してください。

"""


def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "/activate/{}/{}/".format(uid, token)



class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "tel")

    def save(self, commit=True):
        # commit=Falseだと、DBに保存されない
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        print (user.email)
        
        # メール認証を実装するまでの間は無効
        # 確認するまでログイン不可にする
        #user.is_active = False
        account = stripe.Account.create(
        type="custom",
        country="JP",
        email=user.email, #user email
        business_type="individual",
        individual = {
            'email': user.email,
        },
        capabilities={
            'card_payments': {
            'requested': True,
            },
            'transfers': {
            'requested': True,
            },
        },
        tos_acceptance={
            'date': int(time.time()),
            'ip': '8.8.8.8', # Depends on what web framework you're using
        }
        )
        print (account)
        user.is_active = True
        user.stripe_id = account.id
        if commit:
            user.save()
            #activate_url = get_activate_url(user)
            #message = message_template + activate_url
            #user.email_user(subject, message)
            
            point = Point(
                    user = user,
                    point = 0
                    )
            point.save()

        return user
        

def activate_user(uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        return False

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    
    return False
