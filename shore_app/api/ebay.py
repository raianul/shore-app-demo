import requests

from shore_app.app import app


class Ebay(object):

    def __init__(self, callname):
        self.host = app.config.get('EBAY_HOST')
        self.params = app.config.get('EBAY_API_PARAMS')
        self.callname = callname

    def search(self, query, pagesize=None):
        if query:
            self.params['QueryKeywords'] = query
        if pagesize:
            self.params['MaxEntries'] = pagesize
        self.params['callname'] = self.callname
        self.params['SortOrderType'] = 'PricePlusShippingLowest'
        response = requests.get(self.host, params=self.params)
        return response.json()
