#
# Functions for calling a crypto exchange API
#
#

import requests


class callApi:
    #initialise class
    def __init__(self, coinSymbols, currency='usd'):
        #coin symbols can be list or individual
        #coin symbols from constructor are then used to build price list which is built upon opening portfolio or history window
        #handy to build this way as can be used for individual prices or multiple

        self.coinSymbols = coinSymbols
        self.currency = currency


    def getPrices(self):
        #make the call to coingecko api
        #main uri for this is 'https://api.coingecko.com/api/v3/'

        response = requests.get("https://api.coingecko.com/api/v3/coins/list")

        #search for symbol in response and take id
        #coinDetails is dictionary with values { 'id' : x, 'symbol' : x, 'name' : }
        #need this step really as we need to get id as we wont know this
        #ISSUE:
        #   # multiple id's returned, need to be able to single this out - maybe the chain as an input?
        #   # realistically, dont need each individual crypto from history, can just query portfolio list and use that to build our individual prices
        #   #   # from here we can build up a list of {coin : price}

        coinIds = ""
        if isinstance(self.coinSymbols, list):
            for symb in self.coinSymbols: 
                for coin in response.json(): #more efficient to search this way as we arent searching through every single coin
                    if coin['symbol'].upper() == symb:
                        #coinIds.append(coin['id'])
                        coinIds += coin['id'] + ','
                        break
        else:
            coinIds = next(coin for coin in response.json() if coin["symbol"].upper() in self.coinSymbols)

        if coinIds[-1] == ',':
            coinIds = coinIds[:-1] # slice notation to remove final comma

        #now with this id, make a call to a different api to get price (also requires currency)
        #next api allows for multiple coins to get price of, can group ..... cant be a list though, needs to be a string "coin,coin,coin etc" - all one word, append to a string rather than list
        #params are id(s), vs_currencies

        parameters = {'ids' : coinIds, 'vs_currencies' : self.currency}
        response = requests.get("https://api.coingecko.com/api/v3/simple/price", params=parameters)

        coinPriceDetails = response.json()
        
        return coinPriceDetails
                
