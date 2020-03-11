import checksum
import json

json_string = '''{\"ORDERID\":\"C8bMQGQ7XaZHT6\",\"MID\":\"skvJqi01482500655531\",\"TXNID\":\"20200130111212800110168475501223875\",\"TXNAMOUNT\":\"30.00\",\"PAYMENTMODE\":\"DC\",\"CURRENCY\":\"INR\",\"TXNDATE\":\"2020-01-30+09:37:08.0\",\"STATUS\":\"TXN_SUCCESS\",\"RESPCODE\":\"01\",\"RESPMSG\":\"Txn+Success\",\"GATEWAYNAME\":\"HDFC\",\"BANKTXNID\":\"777001699212868\",\"BANKNAME\":\"CHASE+MANHATTAN+BANK+USA-+N.A.\",\"CHECKSUMHASH\":\"qLpTPn83eCUFxiD3vlQILSB5zzhS9E4R4ltwTSSBm34B577cbwh7EwHD8KsB+baSSzD52Qjd\/k1aM72cBEAopp4+31DdfEz6\/bocGDUahHo=\"}'''
obj = json.loads(json_string)
hash = obj['CHECKSUMHASH']
print(checksum.verify_checksum(obj, '@NX%Krpzb5zS@oRV', hash))