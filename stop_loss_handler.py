import email_handler

STOP_LOSS_MAP = {
    'ETH/USD': 15.00,
    'DOT/USD': 0.08,
    'ADA/USD': 0.05,
    'MANA/USD': 0.05,
    'MATIC/USD': 0.05,
    'AVAX/USD': 0.50,
    'LINK/USD': 0.50,
    'ICP/USD': 0.50,
    'ATOM/USD': 0.3,
    'SOL/USDT': 0.50,
    'BTC/USDT': 10.00,
    'ALGO/USDT': 0.05,
    'SHIB/USD': 0.02,
    'DOGE/USDT': 0.02,
    'BAT/USDT': 0.02,
    'KCS/USDT': 0.50,
    'ONE/USDT': 0.20,
    'SHIB/USDT':0.02
}

def get_stop_loss(ticker):
    if ticker not in STOP_LOSS_MAP:
        print("Stop Loss has not been updated for ticker ==> {0} --- using default 0.50")
        return 1.00
    return STOP_LOSS_MAP[ticker]


def is_profitable_sell(amount, sellprice, buy_price, ticker, buyfee):
    # Check if sell price is profitable taking fee estimate into account
    buy_cost = float((amount * buy_price) + buyfee)
    sell_cost = float(amount * sellprice)
    diff = sell_cost - buy_cost
    resultDict = {'buy_cost': buy_cost, 'sell_cost': sell_cost, 'trade_pnl':diff, 'is_profitable': False}

    if diff < get_stop_loss(ticker):
        resultDict['is_profitable'] = False
    else:
        resultDict['is_profitable'] = True

    return resultDict


# if __name__ == "__main__":
#     if not (check_stop_loss('ADA/USD', 'LbCrypto1200Cb')):
#         print("No Unfilled Orders")
#     else:
#         print("Unfilled Order exists")
