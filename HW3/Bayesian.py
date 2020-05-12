import numpy as np
import csv
import arrow
import matplotlib.pyplot as plt
# import requests
# from fake_useragent import UserAgent

alpha = 5e-3
beta = 11.1
degree = 10

dataset = './Dataset'
# data_files = ['GOOG_0.csv', 'GOOG_1.csv', 'GOOG_2.csv', 'GOOG_3.csv', 'GOOG_4.csv', 'GOOG_5.csv', 'GOOG_6.csv',
#               'GOOG_7.csv', 'GOOG_8.csv', 'GOOG_9.csv']
data_files = ['GOOG_else.csv']

absolute_err_all = []
relative_err_all = []


# # from the website API--Alpha vantage to get recently stock data
# def data_getter():
#     URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=VBOSTIUBM79EGTL7"
#     headers = {
#         "User-Agent": UserAgent().random
#     }
#     response = requests.get(url, headers=headers)
#     return response


def read_in_csv(file):
    x_raw = []
    y_raw = []
    x_today = []
    y_today = []
    with open(file) as cf:
        # cf = data_getter()
        reader = csv.DictReader(cf)
        row = reader.__next__()
        # Get the timestamp of today and the price of today's close
        x_today.append(arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp)
        y_today.append(float(row['close']))
        for row in reader:
            # Store each row in the csv file in two array
            timestamp = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
            x_raw.append(timestamp)
            y_raw.append(float(row['close']))
        # Get the first day in the csv file
        first_day = arrow.get(row['timestamp']).replace(tzinfo='US/Pacific').timestamp
        # Calculate how many days are in the csv file
        x_raw = [int((day - first_day) / 86400) for day in x_raw]
        x_today = [int((x_today[0] - first_day) / 86400)]
    return np.asarray(x_raw), np.asarray(y_raw), np.asarray(x_today), np.asarray(y_today)


def phi(x):
    phi = [[x ** i] for i in range(degree + 1)]
    return np.asarray(phi)


def mean(x):
    return beta * phi(x).T.dot(S).dot(np.sum([t * phi(xt) for xt, t in zip(x_train, y_train)], axis=0))[0][0]


def var(x):
    return (1 / beta + phi(x).T.dot(S.dot(phi(x))))[0][0]


for file in data_files:
    print(file)
    file_name = dataset + '/' + file
    x_all, y_all, x_t, y_t = read_in_csv(file_name)
    N = len(x_all)
    x_train = np.arange(0, 1.0, 1.0 / N)
    y_train = y_all[::-1]
    x_test = np.arange(0, 1.0 + 1.0 / N, 1.0 / N)

    # Calculate the formula 1.72
    S_inv = alpha * np.identity(degree + 1) + beta * np.sum([phi(x).dot(phi(x).T) for x in x_train], axis=0)
    S = np.linalg.inv(S_inv)

    # Plot the stock value of the csv file
    plt.plot(x_test, [mean(x) for x in x_test], color='0')
    for x, t in zip(x_train, y_train):
        plt.scatter(x, t, color='b')

    # Predict the next time
    predict_v = mean(x_test[-2])
    variance = var(x_test[-2])
    print("The prediction of N+1 time is", predict_v, "+-", variance)
    print("The real value is", y_t)

    # Calculate the absolute and relative error
    absolute_err = abs(y_t - predict_v)
    relative_err = absolute_err / y_t
    absolute_err_all.append(absolute_err)
    relative_err_all.append(relative_err)
    print("The absolute error is", absolute_err)
    print("The relative error is", relative_err)

    print()
    plt.show()

absolute_mean_err = np.average(absolute_err_all)
ave_relative_err = np.average(relative_err_all)
print("The overall absolute mean error is ", absolute_mean_err)
print("The overall average relative error is ", ave_relative_err)
