"""
 Created by 七月 on 2018/5/13.
"""
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed 


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    client_id = verify_auth_token(token)
    if not client_id:
        return False
    else:
        # request
        g.client_id = client_id
        return True


def verify_auth_token(token):
    """校验token"""
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token is invalid',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token is expired',
                         error_code=1003)
    client_id = data['id']
    return client_id
