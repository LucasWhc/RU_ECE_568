# import pandas as pd
# import numpy as np
# import datetime
# import time
import json

# company_name = ["GOOG", "MSFT", "AAPL", "NVDA", "SBUX", "AMZN", "OVTZ", "IBM", "AMD", "INTC"]
company_name = ["GOOG"]


def get_ema(cps):
    ema1 = cps.copy()
    ema2 = cps.copy()
    for i in range(len(cps)):
        if i == 0:
            ema1[i] = cps[i]
            ema2[i] = cps[i]
        if i > 0:
            ema1[i] = (11 * ema1[i - 1] + 2 * cps[i]) / 13
            ema2[i] = (25 * ema2[i - 1] + 2 * cps[i]) / 27
    return ema1, ema2


def file_reader(comp):
    # get_historical_data(comp)
    with open('/Users/lucifer.w/Documents/568/project/phase1/data/' + comp +
              '_historical_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    test_json = data
    stock_price_close = []
    # stock_price_high = []
    # stock_price_low = []
    # stock_volume = []
    stock_date = []
    for i in test_json:
        stock_price_close.append(i['Close'])
        # stock_price_high.append(i['High'])
        # stock_price_low.append(i['Low'])
        stock_date.append(i['Time'])
        # stock_volume.append(i['Volume'])
    return stock_price_close, stock_date


for comp in company_name:
    cps, dates = file_reader(comp)
    ema12, ema26 = get_ema(cps)
    # print(emas)
    print(type(dates))
