import arrow
import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
# import requests
# from fake_useragent import UserAgent

dataset = './Dataset'
data_files = ['GOOG_0.csv', 'GOOG_1.csv', 'GOOG_2.csv', 'GOOG_3.csv', 'GOOG_4.csv', 'GOOG_5.csv', 'GOOG_6.csv',
              'GOOG_7.csv', 'GOOG_8.csv', 'GOOG_9.csv']
# data_files = ['GOOG_else.csv']

absolute_err_all = []
relative_err_all = []
r2_all = []


# # from the website API--Alpha vantage to get recently stock data
# def data_getter():
#     URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY
#     &symbol=MSFT&outputsize=full&apikey=VBOSTIUBM79EGTL7"
#     headers = {
#         "User-Agent": UserAgent().random
#     }
#     response = requests.get(url, headers=headers)
#     return response


def r2_func(y_test, y):
    return 1-((y_test-y)**2).sum() / ((y.mean() - y)**2).sum()


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


# degrees = [5, 6, 7, 8, 9, 10, 11, 12]
# for degree in degrees:
for file in data_files:
    print(file)
    file_name = dataset + '/' + file
    x_all, y_all, x_t, y_t = read_in_csv(file_name)
    N = len(x_all)
    x_train = np.arange(0, 1.0, 1.0 / N)
    y_train = y_all[::-1]
    x_test = np.arange(0, 1.0 + 1.0 / N, 1.0 / N)

    # Plot the stock value of the csv file
    # plt.plot(x_test, [mean(x) for x in x_test], color='0')
    # for x, t in zip(x_train, y_train):
    #     plt.scatter(x, t, color='b')

    degrees = [13]
    for degree in degrees:
        clf = Pipeline([('poly', PolynomialFeatures(degree=degree)), ('linear', linear_model.Lasso())])
        clf.fit(x_train[:, np.newaxis], y_train)
        y_predict = clf.predict(x_train[:, np.newaxis])
        # plt.plot(x_train, y_train, color='0')
        # for x, t in zip(x_train, y_train):
        #     plt.scatter(x, t, color='b')
        R2 = r2_func(y_predict, y_train)
        r2_all.append(R2)
        predict_v = clf.predict(np.array(x_test[-2]).reshape(1, -1))
        print("The prediction of N+1 time is", predict_v)
        print("The real value is", y_t)
        absolute_err = abs(y_t - predict_v)
        relative_err = absolute_err / y_t
        absolute_err_all.append(absolute_err)
        relative_err_all.append(relative_err)
        print("The absolute error is", absolute_err)
        print("The relative error is", relative_err)
        print("The root mean square error is", R2)
        print('The coefficients are', clf.named_steps['linear'].coef_)
        print()

    # plt.show()

absolute_mean_err = np.average(absolute_err_all)
ave_relative_err = np.average(relative_err_all)
ave_r2 = np.average(r2_all)
print("The overall absolute mean error is ", absolute_mean_err)
print("The overall average relative error is ", ave_relative_err)
print("The overall average root mean square error value is ", ave_r2)
