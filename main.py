from flask import Flask, request, Response

import trade_util
import trades_handler
import constants
import product_map
import secrets_manager
import traceback
import sys


def ugo_chukwu(request):
    bias_msg = ""
    try:
        exc_info = sys.exc_info()
        data = request.get_json()
        api_secrets = secrets_manager.get_coinbase_secrets()

        # Change to Coinbase Ticker Format as Tradingview ticker format is different
        data[constants.TICKER] = product_map.getCoinbaseTickerFormat(data[constants.TICKER])

        print("Recieved Request Details ==>\n {0}".format(data))

        # Validate Request
        if data['passphrase'] != api_secrets.TradingViewAlertSecret:
            print("Invalid passphrase specified. for {0}".format(data[constants.TICKER]))
            return Response(response="Invalid passphrase specified.", status=400)

        # Place Order
        trade_bias = trade_util.get_bias(data)
        bias_msg = "recieved trade bias == {0} for ticker {1}".format(trade_bias, data[constants.TICKER])
        print(bias_msg)
        if trade_bias.upper() == constants.BUY:
            result = trades_handler.buy_product(data)
        elif trade_bias.upper() == constants.SELL:
            result = trades_handler.sell_product(data)
        else:
            return Response(
                status=500,
                response="Unable to successfully handle alerts! Please check the "
                         "application logs for more details. \n{0}".format(bias_msg)
            )

        return {"ticker": data['ticker'],
                'quantity': data['amount'],
                'buy_price': data.get('buyprice', 0.0),
                'sell_price': data.get('sellprice', 0.0),
                'bias': data['bias'],
                'result': result
                }

    except Exception as e:
        print(e)
        return Response(
            status=500,
            response="Unable to successfully process alerts! Please check the "
                     "application logs for more details. \n{0}".format(bias_msg)
        )
    finally:
        print("Exception in maximus_ugochukwu()  ==> \n{0}".format(traceback.print_exception(*exc_info)))
        del exc_info
