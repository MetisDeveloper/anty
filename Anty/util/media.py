import requests
import json
from os import path

# 接続パラメータ
USER_NAME = "gncu94200686"
PASSWORD = "5pFb/8cvA(&5"
TENANT_ID = "bb1da7ddca434cf287ba087513281fff"
URL = 'https://identity.tyo2.conoha.io/v2.0/tokens'
OBJECT_STORAGE = 'https://object-storage.tyo2.conoha.io/v1/nc_bb1da7ddca434cf287ba087513281fff'


def getToken():
    """
    tokenの取得
    """

    headers = {
        'Accept': 'application/json',
    }
    data = '{"auth":{"passwordCredentials":{"username":"%s","password":"%s"},"tenantId":"%s"}}' % (USER_NAME, PASSWORD, TENANT_ID)
    #logger.debug(data)
    response = requests.post(URL, headers=headers, data=data)
    data = response.json()
    return json.dumps(data["access"]["token"]["id"], indent=4)



def uploadObject(file_name, media_path, storage_path):
    """
    オブジェクトのアップロード
    """

    headers = {
        'Accept': 'application/json',
        'X-Auth-Token': getToken().replace('\"', ''),  # tokenの取得
    }
    print (media_path, storage_path)
    with open(media_path, 'rb') as image:
        response = requests.put(OBJECT_STORAGE + storage_path + file_name, headers=headers, data=image)
        print (response)
    return response
