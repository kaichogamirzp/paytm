import requests
import json

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
import checksum

# initialize a dictionary
paytmParams = dict()
mid = "__"
order_id = "EO68ec7eb2J8BY"
password = "___"

# body parameters
paytmParams["body"] = {

	# Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
	"mid" : mid,

	# Enter your order id for which refund was initiated
	"orderId" : order_id,

	# Enter refund id which was used for initiating refund
	"refId" : "EO6BLfIEEljaRV",
}

# Generate checksum by parameters we have in body
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
checksum = checksum.generate_checksum_by_str(json.dumps(paytmParams["body"]), password)

# head parameters
paytmParams["head"] = {

	# This is used when you have two different merchant keys. In case you have only one please put - C11

	# put generated checksum value here
	"signature"	: checksum
}

# prepare JSON string for request
post_data = json.dumps(paytmParams)

# for Staging
url = "https://securegw.paytm.in/v2/refund/status"

# for Production
# url = "https://securegw.paytm.in/v2/refund/status"

response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
print(response)
