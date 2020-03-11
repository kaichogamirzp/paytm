import json
import checksum
import base64
import string
import random
import json
import hashlib

from Crypto.Cipher import AES

__unpad__ = lambda s: s[0:-ord(s[-1])]
IV = "@@@@&&&&####$$$$"


def __decode__(to_decode, iv, key):
    # Decode
    to_decode = base64.b64decode(to_decode)
    # Decrypt
    c = AES.new(key, AES.MODE_CBC, iv)
    to_decode = c.decrypt(to_decode)
    if type(to_decode) == bytes:
        # convert bytes array to str.
        to_decode = to_decode.decode()
    # remove pad
    return __unpad__(to_decode)

def verify_checksum_by_str(param_str, merchant_key, checksum):
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(param_str, merchant_key, salt=salt)
    return calculated_checksum == checksum


RESPONSE_BODY = '''{
    "head": {
        "responseTimestamp": "1581580786826",
        "version": "v1",
        "signature": "5RI8Zu78pCo5OR9cj8cEJ0xM39iWRnUsVuijo657SYRmDHbhm2YESClPDdEa4hKv4ITPy4rNzPB2M4TJTG6c4VG1DBna7iMqI/NaPMIaJ4M="
    },
    "body": {
        "resultInfo": {
            "resultStatus": "S",
            "resultCode": "0000",
            "resultMsg": "Success"
        },
        "txnToken": "8b6c14ad546446b7afb6271206457a451581580786820",
        "isPromoCodeValid": false,
        "authenticated": false
    }
}'''
d = json.loads(RESPONSE_BODY)
print(json.dumps(d['body']))

print(checksum.verify_checksum_by_str(json.dumps(d['body']), "@@oRV", d['head']['signature']))
