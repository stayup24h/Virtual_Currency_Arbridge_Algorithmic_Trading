import requests
import ccxt
import pprint

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
      def __init__(self, api_key, secret_key):
            self.mybinance = ccxt.binance(config={
                  'apiKey': api_key, 
                  'secret': secret_key
                  })

      def buyCoin(self, target_currency, units): #시장가에 매수
            
            order = self.mybinance.create_market_buy_order( target_currency+"/USDT", units )

            return pprint.pprint(order)
      
      def sellCoin(self, target_currency, units): #시장가에 매도
            
            order = self.mybinance.create_market_sell_order( target_currency+"/USDT", units )

            return pprint.pprint(order)
      
      def withdraw(self, target_currency, units, wallet_address): #송금
            return self.Withdraw(code=target_currency, amount=units, address=wallet_address)