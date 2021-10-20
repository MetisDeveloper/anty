import requests
import json

headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer TJGdiKDkx79o1s8F8lZRxuQnQztFJG2rotfPcByUxWEpc/lyRMUbXqq9s819AdpCqaLUXmb3OzlToWwZ0Xe99h7ugssOQr6/y1NZEiqPMyiYu7X+TTTiTu74w33+zIPEPmuj+mw5RnpJmClWuZznXAdB04t89/1O/w1cDnyilFU='
        }

payload = {
        "messages":[
        {
            "type":"text",
            "text":"定期連絡\n\n明日の打ち合わせまでに目標を設定してください。\n改行で区切って複数設定することができます。"
        }
    ]
    }
requests.post("https://api.line.me/v2/bot/message/broadcast", data=json.dumps(payload), headers=headers)
