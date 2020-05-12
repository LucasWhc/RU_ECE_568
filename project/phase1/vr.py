import json

company_name = ["GOOG"]


def file_reader(comp):
    # get_historical_data(comp)
    with open('/Users/lucifer.w/Documents/568/project/phase1/data/' + comp +
              '_historical_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    test_json = data
    stock_volume = []
    stock_price_close = []
    stock_price_open = []
    for i in test_json:
        stock_volume.append(i['Volume'])
        stock_price_open.append(i['Open'])
        stock_price_close.append(i['Close'])
    return stock_volume, stock_price_open, stock_price_close


def get_vr(vos, ops, cps):
    end = len(vos)
    start = end - 24
    avs = 0
    bvs = 0
    cvs = 0
    for i in range(start, end):
        if abs((ops[i] - cps[i]) / cps[i]) < 0.05:
            cvs += vos[i]
        if ops[i] < cps[i]:
            avs += vos[i]
        if ops[i] > cps[i]:
            bvs += vos[i]
    vr = (avs + 0.5 * cvs) / (bvs + 0.5 * cvs)
    return vr


for comp in company_name:
    vos, ops, cps = file_reader(comp)
    vr = get_vr(vos, ops, cps)
    print(vr)
