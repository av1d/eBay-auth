import base64
import os
import requests

from datetime import date
from datetime import datetime
from datetime import timedelta
from requests.structures import CaseInsensitiveDict


# This checks for the last time we refreshed the ACCESS token. If it is expired,
# or if the file doesn't exist, it will grab a new one based on your REFRESH token.
# To find out how to get a refresh token or to find more auth examples, check
# the repo at https://github.com/av1d/eBay-auth
# This software is not created by or endorsed by eBay. Use at your own risk.


# Put your information here. 
refresh_token = ""
appID         = ""
certID        = ""



def getHourNow():
    now = datetime.now()
    dt = now.strftime("%H")
    return dt



def base64_encode(concatenated_credentials):
    my_string = concatenated_credentials
    my_string_bytes = my_string.encode("ascii")
    base64_bytes = base64.b64encode(my_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string



def Refresh():
    # Base64 encode concatenated Cert ID and App ID like: "app666:cert777"
    b64_encoded = base64_encode(appID + ":" + certID)

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = "Basic " + b64_encoded

    # API request.
    data = (
                "grant_type=refresh_token"
                + "&refresh_token="
                + refresh_token
                + "&scope="
                + "https%3A%2F%2Fapi.ebay.com%2Foauth%2Fapi_scope "
                + "https:%3A%2F%2api.ebay.com%2oauth%2api_scope%2sell.account"
    )

    # API response:
    resp = requests.post(
                            "https://api.ebay.com/identity/v1/oauth2/token",
                            headers=headers,
                            data=data
    )

    # save the JSON response
    with open("refresh_token.json", "w") as f:
        f.write(str(resp.text))
    # save the current hour to track when we need to refresh
    # (token good for 2 hours)
    with open("last_token_refresh.log", "w") as f:
        f.write(str(getHourNow()))

    print("Obtained new User Access Token. Saved in refresh_token.json")



def checkToken():

# See if we need to refresh it by checking the last refresh
# time against current time. # Refresh supports 50,000
# requests per day. We'll just do 1 per hour which is plenty.
# See:
# https://developer.ebay.com/api-docs/static/oauth-rate-limits.html
    
    # Check the last time we refreshed:
    if os.path.exists("last_token_refresh.log"):
        with open("last_token_refresh.log", "r") as f:
            contents = f.readline()
            contents = contents.strip()  # strip "\n"
            try:
                lastTime = int(contents)
            except:
                print("File error or file empty.")
                sys.exit(1)
    else:  # if the token file doesn't exist,
        Refresh()  # get a refresh token.
        hourNow = getHourNow()  # Set the variable to the current time.
        lastTime = int(hourNow)

    # Get the current hour
    now = datetime.now()
    dt = now.strftime("%H")
    thisTime = int(dt)

    # Check if there's at least 1 hour difference between last time.
    # 'Not equals' means at least 1 hour difference.
    if (thisTime != lastTime):
        print(
                "More than 1 hour difference since last token retrieved. "
                + "Fetching new one..."
        )
        Refresh()  # get new token



def main():
    checkToken()



if __name__ == '__main__':
    main()
