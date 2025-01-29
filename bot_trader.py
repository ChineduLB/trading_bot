import time

import constants
import email_handler
import exchange_factory
import secrets_manager

api_secrets = secrets_manager.get_coinbase_secrets()


def buy_crypto(data):
    returnResult = {"result": None, constants.OrderDetail: None}

    try:
        # TODO Add logging Buy order to DB here
        ticker = data['ticker']
        amount = data['amount']
        exchangeNm = data['exchange']

        # Place Market Buy Order... No Point in placing limit orders for buy
        place_buy_market_order(ticker, exchangeNm, amount)

        returnResult = {"result": "Submittted Buy Market Order Successfully", constants.OrderDetail: data}
        print(returnResult)

    except Exception as ex:
        print("Error Submiting buy order in bot_trader for {0}".format(ticker))
        print(ex)
    finally:
        return returnResult

def place_buy_market_order(ticker, exchange_name, amount):

    # get Exchange
    exchange = exchange_factory.get_exchange(exchange_name)

    # Place Market Order
    order = exchange.create_market_buy_order(ticker, amount)

    # Fetch Filled Order Detail -- Transition to a separate Thread or use call back
    time.sleep(5)
    filled_order = exchange.fetch_order(order['id'], ticker)
    if (float(filled_order['price']) <= 0.0):
        print("================ PRICE FETCH FAILED !!!!! =================")
        email_handler.send_email("Market Order Price Fetch Failed for order == {0}, ticker = {1), Qty={2}"). \
            format(order['id'], order['symbol'], order['amount'])

    print("Filled Buy Market Order ==> {0}".format(filled_order))



def sell_crypto(data):
    returnResult = {"result": None, constants.OrderDetail: None}
    try:
        ticker = data['ticker']

        quantity =  data['amount']
        sell_price = data['sellprice']
        exchangeNm = data['exchange']

        result_msg = "Try submit Sell Order ticker {0}, Quantity {1} price {2}".format(ticker, quantity, sell_price)
        print(result_msg)

        if (ticker in constants.SellMarketOrderTickers):
            order = place_sell_market_order(ticker, exchangeNm, quantity)
        else:
            exchange_obj = exchange_factory.get_exchange(exchangeNm)
            order = exchange_obj.create_limit_sell_order(ticker, quantity, sell_price)

        # order from exchange is not serializable...
        order = {**data, **order}

        result_msg = "Completed Sell Order Submission for ticker = " \
                     "{0}, Quantity = {1} at price = {2}".format(ticker, quantity, sell_price)

        print("Order == {0}".format(order))

        order['status'] = constants.COMPLETED
        # order is not serializable...
        # orderdetail = getOrderDetail(order, constants.COMPLETED)
        print("{0} \n{1}".format(result_msg, order))

        returnResult = {"result": result_msg, constants.OrderDetail: order}
    except Exception as ex:
        print("Error Submiting sell order  in bot_trader  for {0}".format(ticker))
        print(ex)
    finally:
        return returnResult

def cancel_exitsing_order(exchange_name, order_id, ticker):
    exchange = exchange_factory.get_exchange(exchange_name)
    cancel_order_id = exchange.cancelOrder(order_id, ticker)
    return cancel_order_id


def place_sell_market_order(ticker, exchange_name, quantity):
    # NOTE =============================================================================== NOTE
    # NOTE DO NOT USE THIS -- MARKET BUY AND MARKET SELL TOGETHER ALWAYS RESULTS IN LOSSES NOTE
    # NOTE =============================================================================== NOTE

    # get Exchange
    exchange = exchange_factory.get_exchange(exchange_name)

    # Place Market Order
    order = exchange.create_market_sell_order(ticker, quantity)

    # Fetch Filled Order Detail
    time.sleep(5)
    filled_order = exchange.fetch_order(order['id'], ticker)

    print("Filled Sell Market Order ==> {0}".format(filled_order))

    return filled_order
