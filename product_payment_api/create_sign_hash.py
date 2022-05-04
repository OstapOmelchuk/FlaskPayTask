import hashlib

from product_payment_api.constants import SecretKey


def sign_formation(kwargs):
    sign = ""
    for key in sorted(kwargs.keys()):
        sign += f"{kwargs[key]}:"
    sign = sign[:-1] + SecretKey
    hashed_sign = hashlib.sha256(sign.encode('utf-8')).hexdigest()
    return hashed_sign
