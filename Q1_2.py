import json
from datetime import datetime
import pytz
import collections
import statsmodels.api as statapi
import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

pst_tz = pytz.timezone('US/Pacific') 
hashtags = ['gohawks' 
            ,'gopatriots'
            ,'nfl'
            ,'patriots'
            ,'sb49'
            ,'superbowl'
            ]

def plot(x, para, label, hashtag):
    plt.figure()
    plt.plot(x, para)
    plt.xlabel('n-hour')
    plt.ylabel(label)
    plt.savefig('plot/' + hashtag + '_' + label + '.png')
    plt.clf()
    return 0

def linear_regr(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    result = statapi.OLS(Y, X).fit()

    print(result.summary())

    mse = mean_squared_error(Y, result.predict())
    rmse = sqrt(mse)

    rsquare = result.rsquared

    return rmse, rsquare


def linearReg(tw_per_hour, n, feature):
    X = []
    Y = []
    # 0 1 2 3 
    # 1 2 3
    prev_value = []
    for key, value in tw_per_hour.items():
        # print(key, ' feature = ', tw_per_hour[key])   
        # print(key)
        prev_value += value

    f_len = n*feature
    first = 0
    while 1:
        X.append(prev_value[first:first+f_len])  
        Y.append(prev_value[f_len+first])
        first += feature

        if first + f_len > len(prev_value) -1:
            break

    # Y = Y[n:]
    # print(len(Y))

    # X = X[n-1:-1]   
    # print(len(X[0]))
    
    rmse, rsquare = linear_regr(X, Y)
    return rmse, rsquare
    

def openHashtag(filename, hashtag):
    tw_per_hour = {}
    for i in range(14, 32):
      for j in range(24):
        hr_str = 10000+(i)*100+j
        tw_per_hour[hr_str] = [0, 0, 0, 0, j]
    for i in range(7): 
      for j in range(24):
        if i == 6 and j == 11:
          break
        hr_str = 20000+(i+1)*100+j
        tw_per_hour[hr_str] = [0, 0, 0, 0, j]

    with open(filename,'r') as f:
        tweets = f.readlines()

        for tw in tweets:
            tw = json.loads(tw)
            time_str = datetime.fromtimestamp(tw["citation_date"], pst_tz)
            post_hour = (time_str.month * 100 + time_str.day) * 100 + time_str.hour
            # print(time_str, post_hour)
            rt = tw['metrics']['citations']['total']
            followers = tw['author']['followers']
            if post_hour in tw_per_hour:
                tw_per_hour[post_hour][0] += 1
                tw_per_hour[post_hour][1] += rt
                tw_per_hour[post_hour][2] += followers
                tw_per_hour[post_hour][3] = max(followers, tw_per_hour[post_hour][3])
            else:
                tw_per_hour[post_hour] = [1, rt, followers, followers, post_hour%100]


    tw_per_hour = collections.OrderedDict(sorted(tw_per_hour.items()))
    feature = 5
    _rmse = [] 
    _rsquare = []
    x = list(range(1,25))
    for n in x:
        rmse, rsquare = linearReg(tw_per_hour,n,feature)
        _rmse.append(rmse)
        _rsquare.append(rsquare)

    plot(x, _rmse, 'rmse', hashtag)
    plot(x, _rsquare, 'rsquare', hashtag)

if __name__ == "__main__":
    for hashtag in hashtags:
        print("#" + hashtag)
        openHashtag('tweet_data/tweets_#' + hashtag + '.txt', hashtag)
