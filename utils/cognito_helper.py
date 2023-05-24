import os
import json
import requests
import cognitojwt
from cognitojwt.constants import PUBLIC_KEYS_URL_TEMPLATE

from core.settings.base import settings


class CognitoJWTHelper:

    def __init__(self):
        self.userpool_id = settings.aws_cognito_settings["AWS_USERPOOL_ID"]
        self.region = settings.aws_cognito_settings["AWS_REGION_NAME"]
        self.app_client_id = settings.aws_cognito_settings["AWS_APP_CLIENT_ID"]
        self.id_token = None

    def fetch_public_key_file(self):
        keys_url: str = PUBLIC_KEYS_URL_TEMPLATE.format(self.region, self.userpool_id)
        r = requests.get(url=keys_url)
        keys_response = r.json()
        json_object = json.dumps(keys_response, indent=4)
        with open("JWKS.json", "w") as outfile:
            outfile.write(json_object)

    def _decode(self):
        verified_claims: dict = cognitojwt.decode(
            self.id_token,
            self.region,
            self.userpool_id,
            # app_client_id=self.app_zclient_id,  # Optional
            testmode=True  # Disable token expiration check for testing purposes
        )
        return verified_claims

    def verified(self, id_token):
        self.id_token = id_token
        key_url = os.environ.get('AWS_COGNITO_JWKS_PATH', None)
        try:
            open(key_url, 'r')
        except FileNotFoundError:
            self.fetch_public_key_file()

        try:
            return self._decode()
        except:
            self.fetch_public_key_file()
            return self._decode()
