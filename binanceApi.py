import requests
import pandas as pd

class BinanceCoin: #binance api class, get 계열(코인 가격, 거래량등 개인정보 필요x)
        def getData(self, target_currency): #코인 평균가격 가져오는 함수
            self.url = "https://api.binance.com/api/v3/ticker/price"
            
            self.params = {
                  "symbol": target_currency+"USDT"
            }

            res = requests.get(self.url, params=self.params)
            value = res.json()

            return value
        
class myBinance: #binance api class, post 계열(거래, 송금등 개인정보 필요 o)
      def __init__(self):
            pass