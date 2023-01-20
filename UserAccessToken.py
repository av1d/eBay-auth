#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests, urllib, base64
from urllib.parse import unquote


# v2.0 - av1d
# https://github.com/av1d/eBay-auth
#
# eBay authorization code grant flow for getting a User Access Token.
#
# Constructed from (with many modifications):
# https://forums.developer.ebay.com/questions/40110/ebay-oauth-token-unable-to-exchange-authorization.html
# Wayback backup copy of post: https://web.archive.org/web/20221202201934/https://forums.developer.ebay.com/questions/40110/ebay-oauth-token-unable-to-exchange-authorization.html
#
# This demonstrates how to obtain the User Access Token which is a two-step process.
# Read the documentation here: https://developer.ebay.com/api-docs/static/oauth-authorization-code-grant.html
#
# See RefreshToken.py for an example of how to use the refresh token.
#
# This software is not created by or endorsed by eBay. Use at your own risk.

my_AppID   = ""
my_CertID  = ""
my_Ru_Name = ""

# Function to convert the credentials into a base64 encoded string:
def base64_encode(concatenated_credentials):
    my_string = concatenated_credentials
    my_string_bytes = my_string.encode("ascii")
    base64_bytes = base64.b64encode(my_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

# strip the token from the URL that gets pasted
def stripURL(ebay_url):
    start = ebay_url.find('code') + 5
    end = ebay_url.find('expires', start) - 1
    x = ebay_url[start:end]
    return x


# Define all scopes you want here, space separated:
# Use this scope for the Application Access Token (Shopping API, etc.): https://api.ebay.com/oauth/api_scope
# Do not percent-encode URLs here, it will be done later for you.
scope = "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly https://api.ebay.com/oauth/api_scope"
scope = urllib.parse.quote_plus(scope)

# Format the URL
url = f"""https://auth.ebay.com/oauth2/authorize?client_id={my_AppID}&redirect_uri={my_Ru_Name}&response_type=code&scope={scope}&"""

print("Open this URL in your broswer then copy the resulting URL found in the browser's address bar after you sign in:\n")
print(url)

# NOTE: if you just get a "Thank you" page without needing to click a button to auth
# then you probably have an invalid scope specified and there's probably no token in the URL
# in your address bar. The message from eBay is confusing so beware.

print("\nPaste the URL here then press enter:\n")
consent_code = input()                 # get URL from user
consent_code = stripURL(consent_code)  # extract code from URL
consent_code = unquote(consent_code)   # remove URL encoding


# You must base64 encode this string so it looks like appid:certid but encoded.
encoded_string = base64_encode(my_AppID + ":" + my_CertID)
auth_string = "Basic " + encoded_string    # concatenate so "Basic " is at the beginning of the base64-encoded string

headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": auth_string}
data = {"grant_type": "authorization_code", "code": consent_code , "redirect_uri": my_Ru_Name}
url_token = "https://api.ebay.com/identity/v1/oauth2/token"

resp = requests.post(url_token, headers=headers, data=data)

print("\n")
print(resp.text)

with open("UserAccessToken.json", "w") as f:
    f.write(resp.text)

print("\nToken saved to UserAccessToken.json")
