import httpretty
import requests
import json
from unittest.mock import patch

from shore_app.config import DefaultConfig
from shore_app.tasks import _get_ebay_response


@httpretty.activate()
def test_get_ebay_response():
    with open('tests/data/ebay_response.json', 'r') as fp:
        ebay_resp = json.load(fp)

    httpretty.register_uri(
        httpretty.GET,
        DefaultConfig.EBAY_HOST,
        json.dumps(ebay_resp)
    )

    response = _get_ebay_response('test')

    assert response.get('Ack') == 'Success'
    assert len(response['SearchResult']) == 2


@httpretty.activate()
def test_get_ebay_response_if_no_result():

    resp = {
        "Timestamp": "2021-08-29T09:24:31.770Z",
        "Ack": "Success",
        "Build": "E1157_CORE_APILW2_19110892_R1",
        "Version": "1157",
        "PageNumber": 1,
        "TotalPages": 0,
        "TotalItems": 0,
        "ItemSearchURL": "http://search.sandbox.ebay.com/ws/search/SaleSearch?DemandData=1&fsop=32&satitle=dddr"
    }

    httpretty.register_uri(
        httpretty.GET,
        DefaultConfig.EBAY_HOST,
        json.dumps(resp)
    )

    response = _get_ebay_response('test')

    assert response is None


@httpretty.activate()
def test_get_ebay_response_if_erro():

    resp = {
        "Timestamp": "2021-08-29T09:27:21.976Z",
        "Ack": "Failure",
        "Errors": [
            {
                "ShortMessage": "Application ID invalid.",
                "LongMessage": "Application ID invalid.",
                "ErrorCode": "1.20",
                "SeverityCode": "Error",
                "ErrorClassification": "RequestError"
            }
        ],
        "Build": "E1157_CORE_APILW2_19110892_R1",
        "Version": "1157"
    }

    httpretty.register_uri(
        httpretty.GET,
        DefaultConfig.EBAY_HOST,
        json.dumps(resp)
    )

    response = _get_ebay_response('test')

    assert response is None
