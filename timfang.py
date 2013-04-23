'''
MODULE_NAME: timfang
A lightweight marketwatch API, designed for high-frequency trade algorithms.
'''
import json
import requests
import sys

#instantiate a stock object
class stockObj:
    def __init__(self, tokens, game, element):
        """Initiates a stock object
        @param tokens: retrieve using method get_token
        @param element: the element loaded into stock_input
        """
        self.tokens = tokens
        self.gameURL = 'http://www.marketwatch.com/game/%s/trade/submitorder?week=1' % game
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.ticker = element[0]
        self.game_ticker = 'STOCK-%s-%s' % (element[1], self.ticker)
        self.tradeshares = element[2]
        self.shares = 0
        self.counter = 0
        self.trend = 0
        self.low = -9000
        self.high = 9000
        self.last = 0
        self.action = 0

        self.holding = 0
        self.holdinglow = self.holdinglast = 0
        self.gains = 0


    def transaction(self, shares, action):
        payload = [{
                        'Fuid': self.game_ticker,
                        'Shares': str(shares),
                        'Type': action
                    }]
        resp = json.loads(requests.post(self.gameURL, data = json.dumps(payload), cookies = self.tokens, headers = self.headers).text)
        if resp['succeeded'] == False:
            print "ERROR: Order failed on %s: %s" % (self.ticker, resp['message'])

    def buy(self, shares):
        self.transaction(shares, 'Buy')

    def sell(self, shares):
        self.transaction(shares, 'Sell')

    def short(self, shares):
        self.transaction(shares, 'Short')
        
    def cover(self, shares):
        self.transaction(shares, 'Cover')

def get_tokens(username, password):
    userdata = {
                    "userName": username,
                    "password": password,
                    "remChk": "on",
                    "returnUrl": "/user/login/status",
                    "persist": "true"
                }
    s = requests.Session()
    s.get('http://www.marketwatch.com/')
    s.post('https://secure.marketwatch.com/user/account/logon', data = userdata)
    if s.get('http://www.marketwatch.com/user/login/status').url == \
        "http://www.marketwatch.com/my":
        print (">>login succeeded!")
    else:
        print ("ERROR: failed to authenticate, fatal error!")
        sys.exit(0)
    return s.cookies
