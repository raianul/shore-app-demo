import requests


def zap_started(zap, target):

    # GET POS Token
    # print("Inside Hook.....")
    response = requests.post(
        "https://app-aws.inventorum.com/api/auth/login/",
        data={"email": "raianul.kabir@gmail.com", "password": "Qwe90qwe"},
    )
    pin_token = response.json().get("token")
    # print(f"Got Pin Token - {pin_token}")

    headers = {"Authorization": f"Token {pin_token}"}
    response = requests.post(
        "https://app-aws.inventorum.com/api/pin-login/",
        data={"username": "raianul.kabir@gmail.com", "pin": "1111"},
        headers=headers,
    )
    token = response.json().get("token")
    # print(f"Got Token - {token}")

    pos_access_key = "7bc67d3ff699bfe9a43c3cb0"

    # print("Removing Header.....")
    # zap.replacer.remove_rule(description="Authorization")
    # zap.replacer.remove_rule(description="Shorepay-Access-Key")

    # print("Adding Header..1...")
    zap.replacer.add_rule(
        description="Authorization",
        enabled=True,
        matchtype="REQ_HEADER",
        matchstring="Authorization",
        replacement=f"Token {token}",
        matchregex=False,
        # apikey=apikey
    )

    # print("Adding Header..2...")
    zap.replacer.add_rule(
        description="Shorepay-Access-Key",
        enabled=True,
        matchtype="REQ_HEADER",
        matchstring="Shorepay-Access-Key",
        replacement=pos_access_key,
        matchregex=False,
        # apikey=apikey
    )
    # print("Exit from Hook")
