import bot_trader
import constants
import stop_loss_handler
import trade_util

def sell_product(data):
    # expected return object
    res_data = {"result": None, constants.OrderDetail: None, 'data': data}

    # Fetch Available balances from Exchange -- available_balance -- {cash_bal, cash_total, ticker_balance, ticker_total}
    available_balance = trade_util.fetch_avail_bal(data['ticker'], data['exchange'])

    # if ticker balance < 0 --  no asset for sale
    if available_balance['ticker_total'] < 0.00:
        return res_data # means have nothing to sell

    # update amount available for sale
    data['amount'] = available_balance['ticker_total']

    # Check For open Sell or Buy Orders -- fetch open_orders -
    open_order = trade_util.fetch_open_orders(data['ticker'], data['exchange'])

    # No unfilled sell order and asset to sell exists
    if not open_order['has_open_order']:
        return submit_sell_order(data, res_data)

    # if unfilled buy order exists - return, nothing to sell -- redundant... should not happen as ticker_ bal > 0
    if open_order['side'] == 'buy':
        msg = "unfilled buy order exists ... Nothing to sell for {0} on Exchange {1}"
        print(msg.format(data['ticker'], data['exchange']))
        return res_data

    # if unfilled sell order exists -- cancel existing open order
    if open_order['side'] == 'sell':
        # cancel_order = bot_trader.cancel_exitsing_order(data['exchange'], open_order['id'], open_order['ticker'])
        msg =  "Stop Loss Suspended !!! ...Market moved away from our previous sell position... old price {0} and resubmit at new price {1}"
        # msg = msg + "  Cancel Order id == {2}"
        print(msg.format(open_order['price'], data['sellprice']))

def  submit_sell_order(data, res_data):
    # fetch_my_trades - get last buy ourder to determine buy price and calculate profit n losse
    existing_asset = trade_util.fetch_my_last_trade(data['ticker'], data['exchange'])
    if ((not existing_asset) or existing_asset['side'] != 'buy'):
        msg = "Last trade transaction is not a buy transaction or no previous orders for ticker ==> {0} exiting without Sell !!!"
        print(msg.format(data['ticker']))
        return res_data

    data['buyfee'] = trade_util.get_fee(data['exchange'], existing_asset['fee'])
    data['buyprice'] = existing_asset['price']
    result_dict = {"result": None, constants.OrderDetail: None}

    # is_profitable_sell = {'buy_cost': buy_cost, 'sell_cost': sell_cost, 'trade_pnl':diff, 'is_profitable': False}
    if stop_loss_handler.is_profitable_sell(data['amount'], data['sellprice'], data['buyprice'], data['ticker'], data['buyfee'])[
        'is_profitable']:
        print('Profitable Sale Triggered for ==> {0}  @ ==> {1}'.format(data['ticker'], data['sellprice']))
        result_dict = bot_trader.sell_crypto(data)
    elif data['sellprice'] > data['buyprice']:
        print('market trending UP for {0}, wait for favourable sell price'.format(data['ticker']))
        return res_data
    elif data['ticker'] in constants.SellMarketOrderTickers:
        # Trying this with only SHIB/USDT
        print('market trending Down for {0}, Stop Loss Sale Triggered @ {1}'.format(data['ticker'], data['sellprice']))
        result_dict = bot_trader.sell_crypto(data)
        return result_dict

    print("Completed Sell Order for {0}".format(data['ticker']))
    return result_dict


def buy_product(data):

    print("Start Buy Request for {0} on exchange {1}".format(data['ticker'], data['exchange']))

    # fetch open_orders --> {'id', 'status', 'side', 'price', 'amount', 'filled', 'remaining', 'ticker', 'type', 'datetime', 'has_open_order':True/False  }
    open_orders = trade_util.fetch_open_orders(data['ticker'], data['exchange'])

    # if len(open_orders) == 0
    if not open_orders['has_open_order']: # Happy Path
        return buy_when_no_open_orders(data)
    else: # Open order exist -- check to see if it's a buy or sell order
        return buy_when_open_order_exists(open_orders, data)

def buy_when_no_open_orders(data):
    print("Start buy_when_no_open_orders request for {0}".format(data['ticker']))

    # Fetch -- avial_bals --> {cash_bal, cash_total, ticker_balance, ticker_total}
    avial_bals = trade_util.fetch_avail_bal(data['ticker'], data['exchange'])

    purchase_amount = trade_util.get_amount_to_purchase(avial_bals, data['buyprice'], data['ticker'], data['exchange'])
    if purchase_amount['amount'] > 0.0:
        data['amount'] = purchase_amount['amount']
        bot_trader.buy_crypto(data)
        print("Complete buy_when_no_open_orders request for {0}".format(data['ticker']))
    else:
        print("Exception !!! Not Enough Cash for -- buy_when_no_open_orders for {0}".format(data['ticker']))
    return data


def buy_when_open_order_exists(open_orders, data):
    print("Start buy_when_open_order_exists request for {0}".format(data['ticker']))
    # If Open order is a sell order, means waiting to sell, do nothing
    if open_orders['side'] == 'sell':
        msg = "No available Cash!!!. Unfilled Sell order exists for Ticker=={0}, Exchange=={1}, Price=={2}, Amount=={3}"
        print(msg.format(data['ticker'], data['exchange'], open_orders['price'], open_orders['amount']))
        return data

    # getting here means unfilled buy order exists
    # Market moved away from our previous buy position... cancel and resubmit at new price
    msg = "===== Chasing the market !!!: Cancelling Existing Order for {0} ==> ID == {1} ===="
    print(msg.format(data['ticker'], open_orders['id']))

    # Cancel Existing order
    bot_trader.cancel_exitsing_order(data['exchange'], open_orders['id'], data['ticker'])

    # Fetch -- avial_bals --> {cash_bal, cash_total, ticker_balance, ticker_total}
    avial_bals = trade_util.fetch_avail_bal(data['ticker'], data['exchange'])

    purchase_amount = trade_util.get_amount_to_purchase(avial_bals, data['buyprice'], data['ticker'], data['exchange'])
    if purchase_amount['amount'] > 0.0:
        data['amount'] = purchase_amount['amount']
        bot_trader.buy_crypto(data)
        print("Complete buy_when_open_order_exists request for {0}".format(data['ticker']))
    else:
        print("Exception !!! Not Enough Cash for -- buy_when_open_order_exists for {0}".format(data['ticker']))
    return data


