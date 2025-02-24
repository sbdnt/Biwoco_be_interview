import jwt
from jwt import DecodeError
from jwt.algorithms import RSAAlgorithm

from rest_framework_jwt.settings import api_settings

from django.contrib.auth import authenticate


def get_username_from_payload_handler(payload):
    username = payload.get('sub')
    authenticate(remote_user=username)
    return username


def cognito_jwt_decode_handler(token):
    """
    To verify the signature of an Amazon Cognito JWT, first search for the public key with a key ID that
    matches the key ID in the header of the token. (c)
    https://aws.amazon.com/premiumsupport/knowledge-center/decode-verify-cognito-json-token/

    Almost the same as default 'rest_framework_jwt.utils.jwt_decode_handler', but 'secret_key' feature is skipped
    """
    options = {'verify_exp': api_settings.JWT_VERIFY_EXPIRATION}
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise DecodeError('Incorrect authentication credentials.')

    kid = jwt.get_unverified_header(token)['kid']
    try:
        # pick a proper public key according to `kid` from token header
        public_key = RSAAlgorithm.from_jwk(api_settings.JWT_PUBLIC_KEY[kid])
    except KeyError:
        # in this place we could refresh cached jwks and try again https://immoatlas.atlassian.net/browse/DEV-69
        raise DecodeError('Can\'t find proper public key in jwks')
    else:
        print('here!')
        return jwt.decode(
            token,
            public_key,
            api_settings.JWT_VERIFY,
            options=options,
            leeway=api_settings.JWT_LEEWAY,
            audience=api_settings.JWT_AUDIENCE,
            issuer=api_settings.JWT_ISSUER,
            algorithms=[api_settings.JWT_ALGORITHM]
        )