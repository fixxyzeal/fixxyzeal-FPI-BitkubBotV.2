from bitkub import Bitkub
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# initial obj non-secure and secure
bitkub = Bitkub(api_key=os.environ.get('KEY'),
                api_secret=os.environ.get('SECRET'))

url = 'https://notify-api.line.me/api/notify'
token = os.environ.get('TOKEN')
headers = {'content-type': 'application/x-www-form-urlencoded',
           'Authorization': 'Bearer '+str(token)}


def GetPrice(name):
    result = bitkub.ticker(sym=name)
    price = float(result[name]['last'])
    return price


def GetMyBalances():
    return bitkub.balances()


def GetMyWallet():
    return bitkub.wallet()


def GetMyOrder(name):
    return bitkub.my_open_orders(name)


def CancelOrder(hash):
    result = bitkub.cancel_order(hash=hash)
    return float(result['error'])


def SellOrder(name, amt, rat):
    result = bitkub.place_ask(sym=name, amt=amt, rat=rat, typ='limit')
    return float(result['error'])


def BuyOrder(name, amt, rat):
    result = bitkub.place_bid(sym=name, amt=amt, rat=rat, typ='limit')
    return float(result['error'])


def SendLineNotify(msg):
    r = requests.post(url, headers=headers, data={'message': msg})
    print(r.text)
    return r.text


def Trading(name, targetprofit, targetlost, buyprice):
    # Get Target Price,Trade
    profitcal = 0
    msg = ""
    targetname = 'THB_' + name
    latestprice = GetPrice(targetname)
    print(f'{targetname} Lastest price = {latestprice}')
    rate = latestprice - buyprice
    print(f'Rate = {rate}')
    # Get MyWallet
    wallet = GetMyWallet()
    amt = float(wallet['result'][name])
    print(f'{targetname} in my wallet amount = {amt}')
    balance = float(wallet['result']['THB'])
    print(f'My wallet THB balance = {balance}')

    # CalProfit
    if(amt > 0):
        profitcal = latestprice + targetprofit
        print(f'ProfitCal = {profitcal}')
    # Get Pending Order
    orders = GetMyOrder(targetname)
    print(f'My pending order = {orders}')
    if(any(orders['result'])):
        for order in orders['result']:
            hashkey = order['hash']
            orderRate = float(order['rate'])
            ordertype = order['side']
            profitcal = (orderRate*targetprofit) / 100
            diff = latestprice - orderRate
            print(f'ProfitCal = {profitcal} Different = {diff}')
            if(ordertype == 'SELL'):
                if(diff >= targetprofit):
                    # Cancel Order
                    CancelOrder(hashkey)
                    msg = f'Order {name} Was Cancel Sell'
                    print(msg)
                    SendLineNotify(msg)
            if(ordertype == 'BUY'):
                if(diff <= targetlost):
                    # Cancel Order
                    CancelOrder(hashkey)
                    msg = f'Order {name} Was Cancel Buy'
                    print(msg)
                    SendLineNotify(msg)

    # balance > 0 place order
    if(balance > 0):
        BuyOrder(targetname, balance, rate)
        msg = f'Create Buy Order {name} with rate = {rate} balance = {balance}'
        print(msg)
        SendLineNotify(msg)

    elif (not orders['result']):
        # Create SELL Order
        SellOrder(targetname, amt, profitcal)
        msg = f'Create Sell Order {name} with rate = {profitcal} balance = {balance}'
        print(msg)
        SendLineNotify(msg)

    return "OK"
