import base64
import string
import random
import json
import hashlib

from Crypto.Cipher import AES


IV = "@@@@&&&&####$$$$"
BLOCK_SIZE = 16


__pad__ = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
__unpad__ = lambda s: s[0:-ord(s[-1])]


def __encode__(to_encode, iv, key):
    # Pad
    to_encode = __pad__(to_encode)
    # Encrypt
    c = AES.new(key, AES.MODE_CBC, iv)
    to_encode = c.encrypt(to_encode)
    # Encode
    to_encode = base64.b64encode(to_encode)
    return to_encode.decode("UTF-8")


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


def __id_generator__(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def __get_param_string__(params, escape_refund=True):
    params_string = []
    for key in sorted(params.keys()):
        if("|" in params[key] or (escape_refund == True and "REFUND" in params[key])):
            respons_dict = {}
            exit()
        value = params[key]
        params_string.append('' if value == 'null' else str(value))
    return '|'.join(params_string)


def generate_checksum(param_dict, merchant_key, salt=None):
    params_string = __get_param_string__(param_dict)
    return generate_checksum_by_str(params_string, merchant_key, salt)


def generate_refund_checksum(param_dict, merchant_key, salt=None):
    for i in param_dict:
        if("|" in param_dict[i]):
            param_dict = {}
            exit()
    params_string = __get_param_string__(param_dict, False)
    return generate_checksum_by_str(params_string, merchant_key, salt)


def generate_checksum_by_str(param_str, merchant_key, salt=None):
    params_string = param_str
    salt = salt if salt else __id_generator__(4)
    final_string = '%s|%s' % (params_string, salt)

    hasher = hashlib.sha256(final_string.encode())
    hash_string = hasher.hexdigest()

    hash_string += salt

    return __encode__(hash_string, IV, merchant_key)


def verify_checksum(param_dict, merchant_key, checksum):
    # Remove checksum
    if 'CHECKSUMHASH' in param_dict:
        param_dict.pop('CHECKSUMHASH')

    params_string = __get_param_string__(param_dict, False)
    return verify_checksum_by_str(params_string, merchant_key, checksum)


def verify_checksum_by_str(param_str, merchant_key, checksum):
    paytm_hash = __decode__(checksum, IV, merchant_key)
    salt = paytm_hash[-4:]
    calculated_checksum = generate_checksum_by_str(param_str, merchant_key, salt=salt)
    return calculated_checksum == checksum


if __name__ == "__main__":
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
    print(verify_checksum_by_str('''{\"resultInfo\": {\"resultStatus\": \"S\", \"resultCode\": \"0000\", \"resultMsg\": \"Success\"}, \"txnToken\": \"8b6c14ad546446b7afb6271206457a451581580786820\", \"isPromoCodeValid\": false, \"authenticated\": false}''', "@NX%Krpzb5zS@oRV", d['head']['signature']))