import numpy as np
import pandas as pd

# use pytrends package https://github.com/GeneralMills/pytrends
# 导入 pytrends
import pytrends
from pytrends.request import TrendReq

import matplotlib
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------------------------
# 这个是个简单的用google trend做的交易策略
# 参考这篇文章 https://www.nature.com/articles/srep01684?message-global=remove&utm_source=buffer&utm_medium=twitter&utm_campaign=Buffer:%252BWardPlunet%252Bon%252Btwitter&buffer_share=23ec0&error=cookies_not_supported
# 声明:
#	这只是个非常简单的策略, 没有做过任何严格的统计测试 (比如backtesting)
# ---------------------------------------------------------------------------------------------


# First get google trend data
# We want to get the day to day data
# But the google trend API only support monethly data
# if requesting the time frame longer than 6 month
# Thus we need to import by parts and combine them manually
# Here we import the google trend data from 2011-01-01 to 2018-01-09

# 首先我们需要得到google trend的数据
# 我们这里想得到每天的数据, 但是pytrend默认只返回每月的数据
# 所以我们手动的导入每六个月的数据 最后把他们合并

google_trend_data = []
trends = TrendReq(hl = 'en-US', tz = 360)
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2017-06-01 2018-02-06', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2017-01-01 2017-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2016-06-01 2017-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2016-01-01 2016-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2015-06-01 2016-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2015-01-01 2015-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2014-06-01 2015-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2014-01-01 2014-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2013-06-01 2014-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2013-01-01 2013-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2012-06-01 2013-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2012-01-01 2012-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2011-06-01 2012-01-01', gprop = '')
google_trend_data.append(trends.interest_over_time())
trends.build_payload(['bitcoin'], cat = 0, timeframe = '2011-01-01 2011-06-01', gprop = '')
google_trend_data.append(trends.interest_over_time())


# Normalize the Google Trends Data
n = len(google_trend_data)
renorm_factor = 1.0
for index, item in enumerate(google_trend_data[::-1]):
    if index > 0.0:
        first_entry = item['bitcoin'].values[0]
        renorm_factor *= float(last_entry)/float(first_entry)
        renorm_array = item['bitcoin'].values * renorm_factor
        trend_array.extend(list(renorm_array[1:]))
    else:
        trend_array = list(item['bitcoin'].values)
    last_entry = item['bitcoin'].values[-1]

trend_array = np.array(trend_array)
trend_array = 100.0 * trend_array/trend_array.max()


# ---------------------------------------------------------------------------------------------

# download the bitcoin historical data from https://www.coindesk.com/price/
# or you can use coinmarketcap API

# 我们还需要bitcoin的历史价格数据
# 这里是从coindesk网站下载的csv文件
# 当然也可以用coinmarketcap提供的API

btc_price = pd.read_csv('coindesk-bpi-USD-close_data-2010-07-17_2018-02-06.csv')
# we only need the price data from 2011-01-01 to 2018-01-09
# 因为google trend的数据是从2011-01-01开始的, 所以我们只需要一部分的价格数据
btc_price = btc_price[167:-2] 
btc_price = btc_price['Close Price'].values

# ---------------------------------------------------------------------------------------------

# Now define two functions

# Function to compute the relative change in the google trends
# 定义函数计算google trend的相对变化
def compute_relative_change(trend_array, delta_t):
    total_time_points = len(trend_array)
    relative_change_array = []
    relative_change_ratio_array = []
    for i in range(delta_t, total_time_points):
        previous_mean = np.mean(trend_array[i - delta_t:i])
        relative_change = trend_array[i] - previous_mean # compute absolute value of relative change
        relative_change_ratio = relative_change / previous_mean # compute relative change ratio
        relative_change_array.append(relative_change) 
        relative_change_ratio_array.append(relative_change_ratio)

    relative_change_array = np.array(relative_change_array).flatten()
    relative_change_ratio_array = np.array(relative_change_ratio_array).flatten()
    return relative_change_array, relative_change_ratio_array

# Function to trade
# 定义交易函数

# define function to compute percentage of buy and sell based on
# the relative change ratio
# scale and shift are the controlled parameters
def sigmoid(x, scale, shift = 0.0):
    return 2.0/(1.0 + np.exp(-(x - shift)/scale)) - 1.0

# version 1
# buy and sell according to the sign of relative change
def trade_v1(price_array, trend_array, delta_t):
    relative_change, _ = compute_relative_change(trend_array, delta_t)
    
    cash0 = 1.0
    cash = cash0
    num_btc = 0.0
    price = 0.0
    asset = cash + num_btc * price
    ASSET = []
    PRICE = []
    ACTION = []
    for index, change in enumerate(relative_change):
        if index == 0:
            price0 = price_array[delta_t + index]
            
        price = price_array[delta_t + index]

        if change < 0.0:
            # sell
            ACTION.append('sell')

            if num_btc > 0.0:
                cash += num_btc * price
                num_btc = 0.0
        else:
            # buy
            ACTION.append('buy')

            if cash > 0.0:
                num_btc += cash / price
                cash = 0.0

        asset = cash + num_btc * price
        ASSET.append(asset)
        PRICE.append(price)

    ASSET = np.array(ASSET)/cash0
    PRICE = np.array(PRICE)/price0
    return PRICE, ASSET, ACTION

# version 2
# buy and sell according to the ratio of relative change
def trade_v2(price_array, trend_array, delta_t, scale):
    _, relative_change_ratio = compute_relative_change(trend_array, delta_t)
    
    cash0 = 1.0
    cash = cash0
    num_btc = 0.0
    price = 0.0
    asset = cash + num_btc * price
    ASSET = []
    PRICE = []
    ACTION = []
    for index, change in enumerate(relative_change_ratio):
        if index == 0:
            price0 = price_array[delta_t + index]
            
        price = price_array[delta_t + index]

        if change < 0.0:
            # sell
            ACTION.append('sell')

            sell_ratio = np.abs(sigmoid(change, scale = scale))
            if num_btc > 0.0:
                cash += sell_ratio * num_btc * price
                num_btc = num_btc * (1.0 - sell_ratio)
        else:
            # buy
            ACTION.append('buy')

            buy_ratio = np.abs(sigmoid(change, scale = scale))
            if cash > 0.0:
                num_btc += cash * buy_ratio / price
                cash = cash * (1.0 - buy_ratio)

        asset = cash + num_btc * price
        ASSET.append(asset)
        PRICE.append(price)

    ASSET = np.array(ASSET)/cash0
    PRICE = np.array(PRICE)/price0
    return PRICE, ASSET, ACTION

# version 3
# buy and sell according to the ratio of relative change
# apply different parameters for bull and bear market
def trade_v3(price_array, trend_array, delta_t, scale_bull, scale_bear, shift_bull, shift_bear):
    _, relative_change_ratio = compute_relative_change(trend_array, delta_t)
    trend_smooth = scipy.signal.savgol_filter(trend_array,51,1)
    bull_bear_indicator = trend_smooth[1:] - trend_smooth[:-1]
    
    cash0 = 1.0
    cash = cash0
    num_btc = 0.0
    price = 0.0
    asset = cash + num_btc * price
    ASSET = []
    PRICE = []
    ACTION = []
    for index, change in enumerate(relative_change_ratio):
        if index == 0:
            price0 = price_array[delta_t + index]
            
        price = price_array[delta_t + index]

        if change < 0.0:
            # sell
            ACTION.append('sell')
            
            if bull_bear_indicator[index] > 0.0:
                # bull market
                temp = sigmoid(change, scale = scale_bull, shift = shift_bull)
                if temp <= 0.0:
                    sell_ratio = np.abs(temp)
                else:
                    sell_ratio = 0.0
                #sell_ratio = np.abs(sigmoid(change, scale = scale_bull, shift = shift_bull))
            else:
                # bear market
                temp = sigmoid(change, scale = scale_bear, shift = shift_bear)
                if temp <= 0.0:
                    sell_ratio = np.abs(temp)
                else:
                    sell_ratio = 0.0
                #sell_ratio = np.abs(sigmoid(change, scale = scale_bear, shift = shift_bear))
            
            if num_btc > 0.0:
                cash += sell_ratio * num_btc * price
                num_btc = num_btc * (1.0 - sell_ratio)
        else:
            # buy
            ACTION.append('buy')
            
            if bull_bear_indicator[index] > 0.0:
                # bull market
                temp = sigmoid(change, scale = scale_bull, shift = shift_bull)
                if temp >= 0.0:
                    buy_ratio = np.abs(temp)
                else:
                    buy_ratio = 0.0
                #buy_ratio = np.abs(sigmoid(change, scale = scale_bull, shift = shift_bull))
            else:
                # bear market
                temp = sigmoid(change, scale = scale_bull, shift = shift_bear)
                if temp >= 0.0:
                    buy_ratio = np.abs(temp)
                else:
                    buy_ratio = 0.0
                #buy_ratio = np.abs(sigmoid(change, scale = scale_bear))

            if cash > 0.0:
                num_btc += cash * buy_ratio / price
                cash = cash * (1.0 - buy_ratio)

        asset = cash + num_btc * price
        ASSET.append(asset)
        PRICE.append(price)

    ASSET = np.array(ASSET)/cash0
    PRICE = np.array(PRICE)/price0
    return PRICE, ASSET, ACTION

# TEST AND PLOT
# 测试,画图

# for version 1, the only parameters is the delta_t
# delta_t = 50 is the optimal
hold, strategy1, _ = trade_v1(btc_price, trend_array, delta_t = 50)
_, strategy2, _ = trade_v2(btc_price, trend_array, delta_t = 50, scale = 0.2)
_, strategy3, _ = trade_v3(btc_price, trend_array, delta_t = 50, \
                                 scale_bull = 0.000, scale_bear = 0.3, \
                                 shift_bull = -0.1, shift_bear = -0.1)

fig, ax = plt.subplots()
ax.plot(np.arange(len(hold)), hold, label='Buy and Hold')
ax.plot(np.arange(len(strategy1)), strategy1, label='Google Trends Strategy v1')
ax.plot(np.arange(len(strategy2)), strategy2, label='Google Trends Strategy v2')
ax.plot(np.arange(len(strategy3)), strategy3, label='Google Trends Strategy v3')
ax.set_xlabel('days')
ax.set_ylabel('Return')
ax.set_yscale('log')
plt.legend(loc='upper left', frameon=False)
plt.show()