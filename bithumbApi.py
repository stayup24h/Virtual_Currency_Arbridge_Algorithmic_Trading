import requests
import time
import math
import base64
import hmac, hashlib
import urllib.parse

headers = {"accept": "application/json"}

class BithumbCoin: #빗썸 코인api class
    def __init__(self, name): #class 생성시 이름 받기
        self.name = name
        self.url = "https://api.bithumb.com/public/orderbook/"+self.name+"_KRW"
    
    def getData(self): # 코인 정보 불러오기
        self.response = requests.get(self.url, headers=headers)
        self.response
        return(self.response)


class MyBithumb: # 내 빗썸 관리 class
    api_url = "https://api.bithumb.com"

    def __init__(self, user_api_key, user_api_secret):
        self.api_key = user_api_key
        self.api_secret = user_api_secret

    def body_callback(self, buf):
        self.contents = buf

    def microtime(self, get_as_float = False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())
        
    def usecTime(self):
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]
    
    def bithumbApiCall(self, endpoint, rgParams):
        endpoint_item_array = {
            "endpoint" : endpoint
        }

        uri_array = dict(endpoint_item_array, **rgParams)

        str_data = urllib.parse.urlencode(uri_array)

        nonce = self.usecTime()

        data = endpoint + chr(0) + str_data + chr(0) + nonce
        utf8_data = data.encode('utf-8')

        key = self.api_secret
        utf8_key = key.encode('utf-8')

        h = hmac.new(bytes(utf8_key), utf8_data, hashlib.sha512)
        hex_output = h.hexdigest()
        utf8_hex_output = hex_output.encode('utf-8')

        api_sign = base64.b64encode(utf8_hex_output)
        utf8_api_sign = api_sign.decode('utf-8')

        headers = {
            "Accenpt": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "Api-key": self.api_key,
            "Api-Nonce": nonce,
            "Api-Sign": utf8_api_sign
        }

        url = self.api_url + endpoint

        r = requests.post(url, headers=headers, data=rgParams)
        return r.text