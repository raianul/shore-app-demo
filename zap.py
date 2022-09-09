#!/usr/bin/env python
# A basic ZAP Python API example which spiders and scans a target URL

import time

import requests
from zapv2 import ZAPv2

target = "http://127.0.0.1:8000/api/"
apikey = "jo59obqs9l7si2ushv0rsmvobi"  # Change to match the API key set in ZAP, or use None if the API key is disabled

# GET POS Token
response = requests.post(
    "https://app-aws.inventorum.com/api/auth/login/",
    data={"email": "raianul.kabir@gmail.com", "password": "Qwe90qwe"},
)
pin_token = response.json().get("token")

headers = {"Authorization": f"Token {pin_token}"}
response = requests.post(
    "https://app-aws.inventorum.com/api/pin-login/",
    data={"username": "raianul.kabir@gmail.com", "pin": "1111"},
    headers=headers,
)
token = response.json().get("token")

pos_access_key = "7bc67d3ff699bfe9a43c3cb0"
# By default ZAP API client will connect to port 8080
# zap = ZAPv2(apikey=apikey)
# Use the line below if ZAP is not listening on port 8080, for example, if listening on port 8090
zap = ZAPv2(
    proxies={"http": "http://zaproxy:8090", "https": "http://zaproxy:8090"},
)
# zap.core.new_session(name="testsession", overwrite=True)
# Proxy a request to the target so that ZAP has something to deal with

# print("Accessing Token {}".format(token))
# print("Accessing target {}".format(target))

zap.replacer.remove_rule(description="Authorization")
zap.replacer.remove_rule(description="Shorepay-Access-Key")

zap.replacer.add_rule(
    description="Authorization",
    enabled=True,
    matchtype="REQ_HEADER",
    matchstring="Authorization",
    replacement=f"Token {token}",
    matchregex=False,
    # apikey=apikey
)

zap.replacer.add_rule(
    description="Shorepay-Access-Key",
    enabled=True,
    matchtype="REQ_HEADER",
    matchstring="Shorepay-Access-Key",
    replacement=pos_access_key,
    matchregex=False,
    # apikey=apikey
)

zap.urlopen(target)
# Give the sites tree a chance to get updated
time.sleep(2)

print("Spidering target {}".format(target))
scanid = zap.spider.scan(target)
# Give the Spider a chance to start
time.sleep(2)
while int(zap.spider.status(scanid)) < 100:
    # Loop until the spider has finished
    print("Spider progress %: {}".format(zap.spider.status(scanid)))
    time.sleep(2)

print("Spider completed")

while int(zap.pscan.records_to_scan) > 0:
    print("Records to passive scan : {}".format(zap.pscan.records_to_scan))
    time.sleep(2)

print("Passive Scan completed")

print("Active Scanning target {}".format(target))
scanid = zap.ascan.scan(target)
while int(zap.ascan.status(scanid)) < 100:
    # Loop until the scanner has finished
    print("Scan progress %: {}".format(zap.ascan.status(scanid)))
    time.sleep(5)

# print("Active Scan completed")

# Report the results

# print("Hosts: {}".format(", ".join(zap.core.hosts)))
# print("Alerts: ")
# pprint(zap.core.alerts())
