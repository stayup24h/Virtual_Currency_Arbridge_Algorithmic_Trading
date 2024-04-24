import requests

headers = {"accept": "application/json"}

class Bithumb: #빗썸api class
    def __init__(self, name): #class 생성시 이름 받기
        self.name = name
        self.url = "https://api.bithumb.com/public/ticker/"+self.name+"_KRW"
    
    def getData(self): # 코인 정보 불러오기
        self.response = requests.get(self.url, headers=headers)
        print(self.url)
        return(self.response)

btc = Bithumb("BTC")

print(btc.getData().text)