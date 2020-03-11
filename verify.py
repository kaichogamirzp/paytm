# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import checksum
import json
import requests

# initialize a dictionary
paytmParams = dict()

# Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
paytmParams["MID"] = "__"

# Enter your order id which needs to be check status for
paytmParams["ORDERID"] = "C8bMQGQ7XaZHT6"

# Generate checksum by parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
checksum = checksum.generate_checksum(paytmParams, "@@oRV")

# put generated checksum value here
paytmParams["CHECKSUMHASH"] = checksum

# prepare JSON string for request
post_data = json.dumps(paytmParams)

# for Staging
url = "https://securegw-stage.paytm.in/order/status"

# for Production
# url = "https://securegw.paytm.in/order/status"

response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print(response)