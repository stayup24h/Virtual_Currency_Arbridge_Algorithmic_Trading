import requests
import time
import math
import base64
import hmac, hashlib
import urllib.parse

class BithumbCoin: #빗썸 api class, get 계열(코인 가격, 거래량등 개인정보 필요x)
    headers = {"accept": "application/json"}

    def getData(self, target_currency, payment_currency): # 코인 정보 불러오기
        self.url = f"https://api.bithumb.com/public/ticker/{target_currency}_{payment_currency}"
        self.response = requests.get(self.url, headers=self.headers)
        
        return(self.response)


class MyBithumb: #빗썸 api class, post 계열(거래, 송금등 개인정보 필요 o)
    api_url = "https://api.bithumb.com"

    def __init__(self, user_api_key, user_api_secret): #class 생성시 api key와 secret key 필요
        self.api_key = user_api_key
        self.api_secret = user_api_secret

    def microtime(self, get_as_float = False): #시간 호출 함수
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())
        
    def usecTime(self): #시간을 bithumb이 원하는 표현으로 바꾸는 함수
        mt = self.microtime(False)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]
    
    def myBithumbWallet(self): #내 bithumb 계좌 잔액 불러오는 함수
        rgParams = {
            'endpoint': '/info/balance',
            "currency": "USDC",
        }
        return self.bithumbApiCall(rgParams['endpoint'],rgParams).text
    
    def buyCoin(self, units, ordercurrency, paymentcurrency): #코인 시장가 매수하는 함수(수량, 매수할 코인, 사용할 화페)
        rgParams = {
            'endpoint': '/trade/market_buy',
            'units': units,
            'order_currency': ordercurrency,
            'payment_currency': paymentcurrency
        }
        return self.bithumbApiCall(rgParams['endpoint'], rgParams)
    
    def sellCoin(self, units, ordercurrency, paymentcurrency): #코인 시장가 매도하는 함수 (수량, 매도할 코인, 사용할 화페)
        rgParams = {
            'endpoint': '/trade/market_sell',
            'units': units,
            'order_currency': ordercurrency,
            'payment_currency': paymentcurrency
        }
        return self.bithumbApiCall(rgParams['endpoint'], rgParams)
    
    def withdrawBithumb(self, units, address, destination, currency, net_type, exchange_name, ko_name, en_name): #코인 출금하는 함수(수량, 1차주소, 2차주소, 출금할코인, 출금 네트워크, 출금 거래소명, 수취인 한국이름, 수취인 영어이름)
        rgParams = {
            'endpoint': '/trade/btc_withdrawal',
            'units': units,
            'address': address,
            'destination': destination,
            'currency': currency,
            'net_type': net_type,
            'exchange_name': exchange_name,
            'cust_type': '01',
            'ko_name': ko_name,
            'en_name': en_name
        }
        return self.bithumbApiCall(rgParams['endpoint'], rgParams)
    
    def bithumbApiCall(self, endpoint, rgParams): #bithumApi를 호출하는 함수, rgParams를 세부적으로 설정해준 함수를 호출하는 방식으로 사용
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
        return r