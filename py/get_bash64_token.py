import base64
import json
 
import requests
from httpsig.requests_auth import HTTPSignatureAuth
from datetime import datetime
 
 
def get_auth(key_id, key_secret):
    signature_headers = ['(request-target)', 'accept', 'date']
    auth = HTTPSignatureAuth(key_id=key_id, secret=key_secret, algorithm='hmac-sha256',
                             headers=signature_headers)
    return auth
 
 
def get_header():
    gmt_form = '%a, %d %b %Y %H:%M:%S GMT'
    headers = {
        'Accept': 'application/json',
        'X-JMS-ORG': '00000000-0000-0000-0000-000000000002',
        'Date': datetime.utcnow().strftime(gmt_form)
    }
    return headers
 
 
class UserClient(object):
 
    def __init__(self, base_url, access_key, access_secret):
        self.base_url = base_url
        self.access_key = access_key
        self.access_secret = access_secret
 
    def create_token(self, **data):
        url = f"{self.base_url}/api/v1/authentication/super-connection-token/"
        auth = get_auth(self.access_key, self.access_secret)
        headers = get_header()
        resp = requests.post(url, headers=headers, auth=auth, json=data)
        return resp.json()
 
    def get_connect_token_auth_info(self, token):
        data = {
            "id": token,
            "expire_now": False,
        }
        url = f"{self.base_url}/api/v1/authentication/super-connection-token/secret/"
        access_key = self.access_key
        access_secret = self.access_secret
        auth = get_auth(access_key, access_secret)
        res = requests.post(url, headers=get_header(), auth=auth, json=data)
        return res.json()
 
 
def main():
    base_url = 'https://js4.zevin.xin:20000'
    access_key = '938005a3-9902-4567-bcda-a18c7493ec21'
    access_secret = '6C851trf5iQzlXbTRVV59sVzRmaXzZ7plzF0'
    user_client = UserClient(base_url, access_key, access_secret)
    data = {
        # 注意：在 JumpServer API 中，资源引用（User, Asset, Account 等）必须使用 UUID
        # 使用名称（如 "admin" 或 "root"）会导致 API 返回 Account Not Found
        "user": "6a5628fc-54a8-400c-b186-31e6bd3a30dd",
        "asset": "455c60a4-003c-461c-8429-10b4a291a039",
        "account": "b2fbf1cd-f4dd-4b97-a41b-50778d1f0324",  # 对应账号 root 的 ID
        "protocol": "mysql",
        # connect_method 是必填项，指定连接协议的具体实现
        "connect_method": "mysql",
    }
    token = user_client.create_token(**data)
    print("create token: ", token['id'])
    print("================== get token detail ==================")
    detail = user_client.get_connect_token_auth_info(token['id'])
    print(json.dumps(detail, indent=2, ensure_ascii=False))
    print("================== get token base64 ==================")
    print(base64.b64encode(json.dumps(detail).encode()).decode())
 
 
if __name__ == '__main__':
    main()
   
