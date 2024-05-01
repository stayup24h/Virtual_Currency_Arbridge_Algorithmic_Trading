import requests
import json
import base64
import hmac
import uuid
import httplib2
import hashlib

headers = {"accept": "application/json"}

class CoinoneCoin: # 코인원 api class, get 계열(코인 가격, 거래량등 개인정보 필요 x)
    
    def __init__(self, target_currency): # class 생성 시 이름 받기
        self.target_currency = target_currency
        self.url = f"https://api.coinone.co.kr/public/v2/markets/KRW/{self.target_currency}"

    def getData(self): # 코인 정보 불러오기
        self.response = requests.get(self.url, headers=headers)
        
        return self.response


class MyCoinone:
    ''' 코인원 api class, post 계열(거래, 송금등 개인정보 필요 o)
        
        사용자가 자산확인/주문/출금 메서드를 사용하면 밑에 coinoneApiCall 메서드에서 모두 실행됨
    
    '''
    api_url = "https://api.coinone.co.kr/v2.1/"

    def __init__(self, access_token, secret_key): # class 생성시 access_token과 secret_key 필요
        self.access_token = access_token
        self.secret_key = secret_key


    def orderCoin(self, side, quantity, target_currency, quote_currency): # 코인 시장가 주문하는 함수(매수/매도(Enum: 'BUY'/'SELL'), 수량, 주문할 코인, 마켓 기준 화폐)
        action = "order/"
        payload = {
            'quote_currency': quote_currency,
            'target_currency': target_currency,
            'type': 'MARKET',
            'side': side,
            'qty': quantity,
        }

        return self.coinoneApiCall(action, payload)
    
    
    def buyCoin(self, quantity, target_currency, quote_currency): # 코인 시장가 매수하는 함수(수량, 매수할 코인, 마켓 기준 화폐)
        self.orderCoin('BUY', quantity, quote_currency, target_currency)
    
    def sellCoin(self, quantity, target_currency, quote_currency): # 코인 시장가 매도하는 함수(수량, 매도할 코인, 마켓 기준 화폐)
        self.orderCoin('SELL', quantity, quote_currency, target_currency)


    def get_encoded_payload(self, payload): # API를 부를 떄 필요한 nonce를 payload에 넣음
        payload['nonce'] = str(uuid.uuid4())

        dumped_json = json.dumps(payload)
        encoded_json = base64.b64encode(bytes(dumped_json, 'utf-8'))

        return encoded_json

    def get_signature(self, encoded_payload): # API를 부를 때 필요한 headers의 signature 반환
        signature = hmac.new(self.access_token, encoded_payload, hashlib.sha512)

        return signature.hexdigest()


    def coinoneApiCall(self, action, payload): # coinoneApi를 호출하여 사용자의 명령을 수행
        url = self.api_url + action
        
        payload['access_token'] = self.access_token # payload에 access_token 기입

        encoded_payload = self.get_encoded_payload(payload)

        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': self.get_signature(encoded_payload),
        }

        http = httplib2.Http()
        response, content = requests.post(url, headers=headers, data=payload)

        return content.text

    
