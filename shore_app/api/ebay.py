import requests

from shore_app.config import EBAY_HOST, EBAY_API_PARAMS


class Ebay(object):

    def __init__(self, callname):
        self.host = EBAY_HOST
        self.params = EBAY_API_PARAMS
        self.callname = callname

    def search(self, query, pagesize, callname='findItemsAdvanced'):

        if query:
            self.params['keywords'] = query
        if pagesize:
            self.params['MaxEntries'] = pagesize
        self.params['callname'] = self.callname

        response = requests.get(self.host, params=self.params)
        return response.json()
