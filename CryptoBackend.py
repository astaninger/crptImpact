import requests

class CryptoExchange(object):
    # abstract factory for a crypto exchange
    def __init__(self, exchange=None):
        self.exchange = exchange
    

class Binance(object):
    def __init__(self, key=None):
        self.key = key
        self.baseUrl = 'https://api.binance.com'
        self.exchangeInfo = None
        self.requestWeights  = {} # key = request timestamp value = weights

    # returns True if ping successful, otherwise returns False
    def testConnection(self):
        response = requests.get(self.baseUrl + '/api/v1/ping')
        if response.status_code == 200:
            return True
        else:
            return False

    # gets the limits for how many requests we can make from our API
    # before the server starts to get angry
    def getRateLimits(self):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        return self.exchangeInfo['rateLimits']

    # gets the info for the exchange
    def getExchangeInfo(self):
        response = requests.get(self.baseUrl + '/api/v1/exchangeInfo')
        self.exchangeInfo = response.json()
    
    #gets the order book for the specified symbol
    def getOrderBook(self, symbol=None, limit=100):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            response = requests.get(self.baseUrl + '/api/v1/depth', params=params)
            return response.json()
        return None
    
    #gets recent trades for the specfied symbol
    def getRecentTrades(self, symbol=None, limit=500):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            response = requests.get(self.baseUrl + '/api/v1/trades', params=params)
            return response.json()
        return None

    # get old trades starting from the specified trade id
    # if no trade id specified will get most recent trades
    def getOldTrades(self, symbol=None, limit=500, fromId=None):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            if fromId:
                params['fromId'] = fromId
            response = requests.get(self.baseUrl + '/api/v1/historicalTrades', params=params)
            return response.json()
        return None

    # get ticker for the last 24 hours for a certain symbol
    def get24HourTicker(self, symbol=None):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
            }
            response = requests.get(self.baseUrl + '/api/v1/ticker/24hr', params=params)
            return response.json()
        return None

    # gets latest price ticker for specified symbol
    def getLatestPrice(self, symbol=None):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
            }
            response = requests.get(self.baseUrl + '/api/v3/ticker/price', params=params)
            return response.json()
        return None

    # gets best trade for specified symbol
    def getBestOrderBookForSymbol(self, symbol=None):
        if not self.exchangeInfo:
            self.getExchangeInfo()
        # check if trade type is available for this exchange
        found = next((item for item in self.exchangeInfo['symbols'] if item['symbol'] == symbol), None)
        if found:
            params = {
                'symbol': symbol,
            }
            response = requests.get(self.baseUrl + '/api/v3/ticker/bookTicker', params=params)
            return response.json()
        return None 


if __name__ == '__main__':
    pass

