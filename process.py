import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/

mid = "__"
order_id = "random_18"
password = "__"
# initialize a dictionary
paytmParams = dict()

# body parameters
paytmParams["body"] = {

    # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    "mid" : mid,

    # Find your Website Name in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    "paymentMode" : "DEBIT_CARD",

    # Enter your unique order id
    "orderId" : order_id,
    "requestType":"NATIVE",

    # on completion of transaction, we will send you the response on this URL
    "cardInfo" : "|4280902033766247|527|062023",

    # Order Transaction Amount here
}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys

# head parameters
paytmParams["head"] = {

    # put generated checksum value here
    "channelId"	: "WEB",
    "txnToken": "b074f6a453644c538f41dbc36f8b9e311583125152266"
}

# prepare JSON string for request
post_data = json.dumps(paytmParams)
print(post_data)

# for Staging
url = "https://securegw.paytm.in/theia/api/v1/processTransaction?mid={}&orderId={}".format(mid, order_id)
print(url)

response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print(response)
