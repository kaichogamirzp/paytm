import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import checksum

# initialize a dictionary
paytmParams = dict()

mid = "__"
order_id = "ENEDUimIBaBSmI"
password = "__"

# body parameters
paytmParams["body"] = {

    # for custom checkout value is 'Payment' and for intelligent router is 'UNI_PAY'
    "refId" : "poqwea",

    # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    "mid" : mid,

    # Find your Website Name in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    "refundAmount": "1",
    # Enter your unique order id
    "orderId" : order_id,

    # on completion of transaction, we will send you the response on this URL
    "txnId" : "20200302111212800110168160916942520",
    "txnType":"REFUND",

}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
hash = checksum.generate_checksum_by_str(json.dumps(paytmParams["body"]), password)
print('here')
print(hash)

# head parameters
paytmParams["head"] = {

    # put generated checksum value here
    "signature"	: hash,
    "clientId": "C11",
}

# prepare JSON string for request
post_data = json.dumps(paytmParams)
print(post_data)

# for Staging
# url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format(mid, order_id)

# for Production
url = "https://securegw.paytm.in/refund/apply"
print(url)

response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print((json.dumps(response)))
# print(checksum.verify_checksum_by_str(json.dumps(response['body']), "@NX%Krpzb5zS@oRV", response['head']['signature']))
