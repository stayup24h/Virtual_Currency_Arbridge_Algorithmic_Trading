import bithumbApi

myBithum = bithumbApi.MyBithumb("api_key", "sec_key")

rgParams = {
    'endpoint': '/info/balance',
    "currency": "ALL",
}

print(myBithum.bithumbApiCall(rgParams['endpoint'],rgParams).text)