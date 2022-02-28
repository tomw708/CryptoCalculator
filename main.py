#
# MAIN FILE FOR CRYPTOCALCULATOR
#
# essentially main aim is to see monetary position of each purchase i have made compared to the current date
# can see when was a good time to invest and when was a bad time
# 
#

import PySimpleGUI as sg
import os.path
from pathlib import Path
import helpers 
from callAPI import callApi

######
#VARIABLES
purchaseHistory = []
portfolioList = []
#firstly check if saved data is present
dataFilePath = Path('data/savedData.txt')
dataFilePath.touch(exist_ok=True)

######

#####################################
#FUNCTIONS

def get_history_list():
    #first read saved data and extract each piece of data
    purchaseHistory.clear()
    dataFile = open(dataFilePath, 'r')
    for line in dataFile:
        coinName, coinSymbol, coinCost, coinAmount, coinPrice = line.rstrip('\n').split(',')
        purchaseHistory.append([coinName, coinSymbol, coinCost, coinAmount, coinPrice])
    dataFile.close()

def make_history_window(position=(0,0)):
    get_history_list()
    layoutHistory =[[sg.Table( values=purchaseHistory,
                                headings=["Coin Name", "Coin Symbol", "Money Spent", "Amount of Coins Received", "Coin Price"],
                                max_col_width=30,
                                auto_size_columns=True,
                                display_row_numbers=True,
                                num_rows=len(purchaseHistory),
                                tooltip="Crypto Purchase History",
                                key='purchaseHistoryTable')],
                    [sg.InputText(do_not_clear=False, key='historySymbolFilter')],   #want to be able to filter by symbol, as well as change order of history
                    [sg.Button("Filter")]]

    return sg.Window(title="Purchase History", layout=layoutHistory, location=(position[0], position[1]), margins=(200,100)).Finalize()

def get_portfolio_list():
    #get coin name, symbol and total price from saveddata
    #portfolio will look like [[coinName, coinSymbol, totalSpent, totalCoins, totalWorthNow(once worked out how to connect API)]]
    portfolioList.clear()
    dataFile = open(dataFilePath, 'r')
    for line in dataFile:
        found = False
        coinName, coinSymbol, coinCost, coinAmount, coinPrice = line.rstrip('\n').split(',')
        #if coin is already in portfolio, add to the total of that coin
        for i in range(len(portfolioList)):
            if portfolioList[i][1] == coinSymbol:
                portfolioList[i][2] += float(coinCost)
                portfolioList[i][3] += float(coinAmount)
                found = True
                break
        if found ==  False:          
            portfolioList.append([coinName, coinSymbol, float(coinCost), float(coinAmount)])

    dataFile.close()


def make_portfolio_window(position=(0,0)):
    #base each token off of its unique symbol
    get_portfolio_list()
    layoutPortfolio =[[sg.Table( values=portfolioList,
                                headings=["Coin Name", "Coin Symbol", "Total Spent", "Total Coins"],
                                max_col_width=30,
                                auto_size_columns=True,
                                display_row_numbers=True,
                                num_rows=len(portfolioList),
                                tooltip="Crypto Portfolio",
                                key='portfolioTable')]]
    return sg.Window(title="Portfolio", layout=layoutPortfolio, location=(position[0], position[1]), margins=(200,100)).Finalize()



#####################################
#main steps

#create first window
layoutMain1 = [ [sg.Text("CryptoCalculator")], 
            [sg.Text("Coin Name: ")],
            [sg.InputText(do_not_clear=False, key='coinName')],
            [sg.Text("Symbol: ")],
            [sg.InputText(do_not_clear=False, key='coinSymbol')],
            [sg.Text("Purchase cost: ")],
            [sg.InputText(do_not_clear=False, key='coinCost')],
            [sg.Text("Amount of coins received: ")],
            [sg.InputText(do_not_clear=False, key='coinAmount')],
            [sg.Text("Coin price at time of purchase: ")],
            [sg.InputText(do_not_clear=False, key='coinPrice')],
            [sg.Button("Add Purchase")],
            [sg.Button("View Portfolio")],
            [sg.Button("Purchase history")],
            [sg.Button("Call API")]]

#main window screen, layout list of elements on screen
layoutMain = [[ sg.Column(layoutMain1, element_justification='c')]]
            

windowMain, windowPurchaseHistory, windowPortfolio = sg.Window(title="CryptoCalculator", layout=layoutMain, margins=(400,200)).Finalize(), None, None


# event loop, wait for something to happen
while True:
    eventMain, valuesMain = windowMain.read()
    # Close window
    if eventMain == sg.WIN_CLOSED:
        break
    
    #get input
    if eventMain == "Add Purchase":
        valid = True
        coinName = valuesMain['coinName']
        coinSymbol = valuesMain['coinSymbol'].upper()
        coinCost = valuesMain['coinCost']
        coinAmount = valuesMain['coinAmount']
        coinPrice = valuesMain['coinPrice']

        #validate all is there
        if bool(coinName) == False or bool(coinSymbol) == False or bool(coinCost) == False or bool(coinAmount) == False or bool(coinPrice) == False:
            sg.Popup('Please fill in all boxes.')
            valid = False

        #make sure the input is a float where necessary
        if not helpers.is_float(coinCost) or not helpers.is_float(coinAmount) or not helpers.is_float(coinPrice):
            sg.Popup('Purchase cost, amount bought, and coin price must be numbers.')
            valid = False

        if valid == True:
            #write data to data file
            dataFile = open(dataFilePath, 'a')
            dataFile.write( coinName + ',' + coinSymbol + ',' + coinCost + ',' + coinAmount + ',' + coinPrice + '\n')
            dataFile.close()
            sg.Popup('Purchase added to log.')
            
            #refresh open windows with updated data
            if windowPurchaseHistory != None:
                a = windowPurchaseHistory.CurrentLocation()
                windowPurchaseHistory.close()
                make_history_window(a)

            if not windowPortfolio != None:
                a = windowPortfolio.CurrentLocation()
                windowPortfolio.close()
                make_portfolio_window(a)


    #open purchase history window
    elif eventMain == "Purchase history":
        windowPurchaseHistory = make_history_window()
        

    #open portfolio window
    elif eventMain == "View Portfolio":
        windowPortfolio = make_portfolio_window()

    elif eventMain == "Call API":
        if windowPurchaseHistory == None:
            get_history_list()
        if windowPortfolio == None:
            get_portfolio_list()
        symbols = []
        for coin in portfolioList:
            symbols.append(coin[1])
        cApi = callApi(symbols)
        print(cApi.getPrices())

        

    

windowMain.close()