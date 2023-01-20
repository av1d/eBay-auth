#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import requests
from requests.structures import CaseInsensitiveDict


"""
    Request REFRESH token from ebay.
    This is not a User Access Token. Check UserAccessToken.py for an example of that grant flow.
    See: https://github.com/av1d/eBay-auth for more examples
    
    This software is not created by or endorsed by eBay. Use at your own risk.
"""

appID  = ""
certID = ""
concat = appID + ":" + certID

refresh_token = ""

url = "https://api.ebay.com/identity/v1/oauth2/token"

# Function to convert the credentials into a base64 encoded string:
def base64_encode(concatenated_credentials):
    my_string = concatenated_credentials
    my_string_bytes = my_string.encode("ascii")
    base64_bytes = base64.b64encode(my_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

b64_encoded = base64_encode(concat)

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Authorization"] = "Basic " + b64_encoded

data = "grant_type=refresh_token" + "&refresh_token=" + refresh_token + "&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope https:%3A%2F%2api.ebay.com%2oauth%2api_scope%2sell.account"


resp = requests.post(url, headers=headers, data=data)

print(resp.text)
