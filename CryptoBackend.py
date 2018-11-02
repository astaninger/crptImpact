import requests
from watson_developer_cloud import AssistantV1
from json import dumps

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
    functionResponses = {}
    exchange = Binance()
    # assistant = AssistantV2(
    #     username="",
    #     password="",
    #     url="",
    #     version=""
    # )
    # If service instance provides API key authentication
    assistant = AssistantV1(
        version='2018-07-10',
        ## url is optional, and defaults to the URL below. Use the correct URL for your region.
        iam_apikey='XUT79VvWy5Qg610kk-kerlwexbFBDsL5-1fPJy64E73o'
    )

    assistantId=None
    sessionId=None

    #response = assistant.list_workspaces().get_result()

    functionCalls = {
        'latestPrice': exchange.getLatestPrice,
        'bestTrade': exchange.getBestOrderBookForSymbol,
        '24HrSummary': exchange.get24HourTicker,
        'exchangeInfo': exchange.getExchangeInfo,
        'recentTrades': exchange.getRecentTrades
    }
    
    # assistant.delete_session("", "").get_result()

    # handles talking to watson through watsons api and uses responses 
    # as a method for deciding what to call in binance api
    def talkToWatson(response = None, context = None, first = True):
        resp = None
        if first:
            message = assistant.message(
                workspace_id="e6a0976e-6ea7-4cf0-a9ac-6387c76261d9",
                input={
                    'text': 'welcome'
                }           
                ).get_result()
            text = message['output']['text'] if len(message['output']['text']) == 0 else message['output']['text'][0]
            resp = input(text)
            talkToWatson(resp, None, False)
        else:
            message = assistant.message(
                workspace_id="e6a0976e-6ea7-4cf0-a9ac-6387c76261d9",
                input={
                    'text': response
                },
                context = context           
                ).get_result()
            text = message['output']['text'] if len(message['output']['text']) == 0 else message['output']['text'][0]
            if text == 'exit':
                print('Goodbye!')
                return
            
            splitText = [0, 0] if len(text) == 0 else text.split(':')
            if splitText[0] in functionCalls:
                print(functionCalls[splitText[0]](splitText[1]))
                talkToWatson()
            else:
                resp = input(text)
                talkToWatson(resp, message['context'], False)

        return
                
    talkToWatson()
        

        





