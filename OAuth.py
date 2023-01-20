#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import requests
from requests.structures import CaseInsensitiveDict


"""
    Get eBay OAUTH token from AppID and CertID for Shopping API
    
    This is not a User Access Token. Check UserAccessToken.py for an example of that grant flow.
    Send AppID + CertID base64 encoded with colon between like this, no spaces:
    appid:certid
    The encoded credentials go in the "Authorization: Basic" header after "Basic".
    Example: "Authorization: Basic MY-SUPER-MAGIC-ENCODED-TOKEN".
    Resulting token is good for 2 hours. Use for Shopping API, etc.

    https://github.com/av1d/eBay-auth

    This software is not created by or endorsed by eBay. Use at your own risk.
"""


## SETTINGS:
# Your App ID / Client ID:
appID  = ""
# Your Client ID / Client secret:
certID = ""
## END SETTINGS

concat = appID + ":" + certID

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

# Define your scopes here.
# URLs are space-separated, URL encoded.
data = "grant_type=client_credentials&scope=https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope https:%3A%2F%2api.ebay.com%2oauth%2api_scope%2sell.account"


resp = requests.post(url, headers=headers, data=data)

print(resp.text)
