
import os
import json
from urllib import request

COGNITO_AWS_REGION = 'eu-central-1'
COGNITO_USER_POOL = 'eu-central-1_bUFIXsrqe'
# Provide this value (id of Cognito App Client) if `id_token` is used for authentication (it contains 'aud' claim).
# `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
COGNITO_AUDIENCE = '2bdgd681nmmnickj0coq0j1oq1'
COGNITO_POOL_URL = None  # will be set few lines of code later, if configuration provided

rsa_keys = {}
# To avoid circular imports in future, we keep this logic here.
# On django init we download jwks public keys which are used to validate jwt tokens.
# For now there is no rotation of keys (and Cognito haven't still implemented it...)
if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    COGNITO_POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}'.format(COGNITO_AWS_REGION, COGNITO_USER_POOL)
    pool_jwks_url = COGNITO_POOL_URL + '/.well-known/jwks.json'
    jwks = json.loads(request.urlopen(pool_jwks_url).read())
    rsa_keys = {key['kid']: json.dumps(key) for key in jwks['keys']}


JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'core.jwt_decode.get_username_from_payload_handler',
    'JWT_DECODE_HANDLER': 'core.jwt_decode.cognito_jwt_decode_handler',
    'JWT_PUBLIC_KEY': rsa_keys,
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': COGNITO_AUDIENCE,
    'JWT_ISSUER': COGNITO_POOL_URL,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}