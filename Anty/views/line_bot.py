from django.shortcuts import render
from django.http import HttpResponse
import json
import datetime
import base64
import requests as R
import sys
from django.views.decorators.csrf import csrf_exempt

from ..line_bot.line_message import LineMessage
import traceback
import logging
from ..models import Line_user
from linebot import WebhookHandler

logging.basicConfig(filename="/Anty/main/Anty/app.log")
logger = logging.getLogger(__name__)

handler = WebhookHandler(channel_secret="3b9b10b4379ef3b8b9f629e878dbcd3d")

@csrf_exempt
def index(requests):
    if requests.method == 'POST':
        request = json.loads(requests.body.decode('utf-8'))
        signature = requests.META["HTTP_X_LINE_SIGNATURE"]
        body = requests.body.decode("utf-8")
        try:
            handler.handle(body, signature)
        except:
            return HttpResponse("faild")
        for event in request['events']:
            data = event
            # 初回のDB登録
            if data["type"] == "follow":
                line_id = data["source"]["userId"]
                if not (Line_user.objects.filter(line_id=line_id)):
                    user = Line_user(
                            user = None,
                            name = None,
                            line_id = line_id,
                            message_status = 0,
                    ).save()
                else:
                    user = Line_user.objects.filter(line_id=data["source"]["userId"]).first()
                    user.message_status = 0
                    user.save()
                    message = [
                        {
                            "type": "text",
                            "text": f"Info\n\n過去に登録があったためデータベースへの登録は行いませんでした。"
                        }
                        ]
            elif data["type"] == "message":
                user = Line_user.objects.filter(line_id=data["source"]["userId"]).first()
                if user.message_status == 0:
                    password = data['message']['text'].strip()
                    if password == "e3NbciXq/Zt_":
                        user.message_status = 1
                        user.save()
                        message = [
                                {
                                    "type": "text",
                                    "text": f"パスワード認証が完了しました。\n\n次にLINE一斉配信を行う際の名前を送信してください。"
                                    }
                                ]
                    else:
                        message = [
                                {
                                    "type": "text",
                                    "text": f"パスワード認証に失敗しました"
                                    }
                                ]
                elif user.message_status == 1 :
                    name = data['message']['text'].strip()
                    user.name = name
                    user.message_status = 2
                    user.save()
                    message = [
                            {
                                "type": "text",
                                "text": f"名前を「{name}」で設定しますか？\nよろしければ「はい」を、変更する場合はそれ以外のメッセージを送信してください。"
                                }
                            ]
                elif user.message_status == 2 :
                    is_agree = data['message']['text'].strip()
                    if is_agree == "はい":
                        user.message_status = 3
                        user.save()
                        message = [
                                {
                                    "type": "text",
                                    "text": f"名前を「{user.name}」で設定しました。\n\nアカウントの機能が解放されました。詳しくは「ヘルプ」と送信してください。"
                                    }
                                ]
                    else:
                        user.message_status = 1
                        user.save()
                        message = [
                                {
                                    "type": "text",
                                    "text": f"再度名前を送信してください。"
                                    }
                                ]
            
                elif user.message_status == 3 :
                    text = data['message']['text'].strip()
                    if text == "ヘルプ":
                        message = [
                                        {
                                            "type": "text",
                                            "text": f"・一斉送信したい場合は「一斉送信」\n・次回打ち合わせの目標を設定するときは「目標設定」\n・今週の目標を確認したい/達成チェックにするには「目標確認」と入力してください。"
                                            }
                                        ]
                    elif text == "一斉送信":
                        user.message_status = 4
                        user.save()
                        message = [
                                        {
                                            "type": "text",
                                            "text": f"一斉送信したい文章を送信してください。送信後に配信確認を挟みます。\n写真などは対応していません。送信元は自動的に挿入されます。\nキャンセルしたい場合は「キャンセル」と送信してください。"
                                            }
                                        ]


                elif user.message_status == 4:
                    if data['message']['text'].strip() == "キャンセル":
                        user.message_status = 3
                        user.save()
                        message = [
                                        {
                                            "type": "text",
                                            "text": "キャンセルされました"
                                            }
                                        ]
                    else:
                        user.message_status = 5
                        user.save()
                        message = [
                                        {
                                            "type": "text",
                                            "text": f"一斉送信\nfrom {user.name}\n\n{data['message']['text']}"
                                            },
                                        {
                                            "type": "text",
                                            "text": "で送信します。よろしいですか?\nよろしければ「はい」を、変更する場合はそれ以外のメッセージを送信してください。"
                                            }
                                        ]
                        user.broadcast = data['message']['text']
                        user.save()
                elif user.message_status == 5:
                    if data['message']['text'].strip() == "はい":
                        headers = {
                                'content-type': 'application/json',
                                'Authorization': 'Bearer TJGdiKDkx79o1s8F8lZRxuQnQztFJG2rotfPcByUxWEpc/lyRMUbXqq9s819AdpCqaLUXmb3OzlToWwZ0Xe99h7ugssOQr6/y1NZEiqPMyiYu7X+TTTiTu74w33+zIPEPmuj+mw5RnpJmClWuZznXAdB04t89/1O/w1cDnyilFU='
                                }

                        payload = {
                                "messages":[
                                {
                                    "type":"text",
                                    "text":f"一斉配信\nfrom {user.name}\n\n{user.broadcast}"
                                }
                            ]
                            }
                        R.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(payload), headers=headers)
                        user.message_status = 3
                        user.broadcast = None
                        user.save()
                        continue
            
            else:
                continue
            line_message = LineMessage(message)
            reply_token = data['replyToken']
            line_message.reply(reply_token)

        return HttpResponse("ok")
    else:
        return HttpResponse("Use GET")
