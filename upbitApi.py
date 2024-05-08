import os
import jwt
import hashlib
import uuid
from urllib.parse import urlencode, unquote
import requests

class Upbit: # 업비트 시장가 api를 불러오는 클래스
    def getData(self, target_currency): # 코인의 시장가 데이터를 json으로 반환
        self.url = f"https://api.upbit.com/v1/ticker/?markets=KRW-{target_currency}"
        self.headers = {"accept": "application/json"}
        self.response = requests.get(self.url, headers=self.headers)

        return self.response.json()[0]
    
class MyUpbit: # 개인 key가 필요한 기능을 모아놓은 클래스
    def __init__(self, access_key, secret_key, server_url):
        self.access_key = access_key
        self.secret_key = secret_key
        self.server_url = server_url

    def orderCoin(self, side, quantity, target_currency): # 코인 시장가 주문하는 함수(매수/매도(Enum: 'BUY'/'SELL'), 수량, 주문할 코인)
        if side == 'BUY': # side('BUY'/'SELL')를 api에 맞게 변환
            side = 'bid'
            ord_type = 'price'
        elif side == 'SELL':
            side = 'ask'
            ord_type = 'market'
        else: # side가 'BUY' 또는 'SELL'이 아니면 오류 출력
            print("error")
            raise ValueError("side parameter should be either 'BUY' or 'SELL'. ")


        params = {
            'market': target_currency,
            'side': side,
            'volume': quantity,
            'price': quantity*Upbit().getData(target_currency).trade_price,
            'ord_type': ord_type
        }

        return self.apiCall(self, params)
        
    def buyCoin(self, quantity, target_currency): # 코인 시장가 매수하는 함수(수량, 주문할 코인)
        return self.orderCoin(self, "BUY", quantity, target_currency)
    
    def sellCoin(self, quantity, target_currency): # 코인 시장가 매도하는 함수(수량, 주문할 코인)
        return self.orderCoin(self, "SELL", quantity, target_currency)
    

    def apiCall(self, params): # 업비트 API 호출
        access_key = os.environ[self.access_key]
        secret_key = os.environ[self.secret_key]
        server_url = os.environ[self.server_url]

        query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
            'query_hash': query_hash,
            'query_hash_alg': 'SHA512',
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {
        'Authorization': authorization,
        }

        res = requests.post(server_url + '/v1/orders', json=params, headers=headers)
        
        return res.json()[0]