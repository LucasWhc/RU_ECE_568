import json
import ema

# company_name = ["GOOG", "MSFT", "AAPL", "NVDA", "SBUX", "AMZN", "OVTZ", "IBM", "AMD", "INTC"]
company_name = ["GOOG"]


def file_reader(comp):
    # get_historical_data(comp)
    with open('/Users/lucifer.w/Documents/568/project/phase1/data/' + comp +
              '_historical_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    test_json = data
    stock_price_close = []
    # # stock_price_high = []
    # # stock_price_low = []
    # # stock_volume = []
    # stock_date = []
    for i in test_json:
        stock_price_close.append(i['Close'])
    #     # stock_price_high.append(i['High'])
    #     # stock_price_low.append(i['Low'])
    #     stock_date.append(i['Time'])
    #     # stock_volume.append(i['Volume'])
    return stock_price_close


def get_macd(cps):
    ema12, ema26 = ema.get_ema(cps)
    diff = cps.copy()
    dea = cps.copy()
    bar = cps.copy()
    for i in range(len(cps)):
        if i == 0:
            diff[i] = 0
            dea[i] = 0
            bar[i] = 0
        if i > 0:
            diff[i] = ema12[i] - ema26[i]
            dea[i] = dea[i - 1] * 0.8 + diff[i] * 0.2
            bar[i] = 2 * (diff[i] - dea[i])
    return diff, dea, bar


for comp in company_name:
    stock = file_reader(comp)
    diff, dea, bar = get_macd(stock)
    # print(diff)
    # print(dea)
    # print(bar)
