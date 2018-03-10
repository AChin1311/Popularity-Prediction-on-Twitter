import json
from datetime import datetime
import pytz
import collections
import statsmodels.api as statapi
import numpy as np

pst_tz = pytz.timezone('US/Pacific') 
hashtags = ['gohawks' 
            # ,'gopatriots'
            # ,'nfl'
            # ,'patriots'
            # ,'sb49'
            # ,'superbowl'
            ]

def linearReg(tw_per_hour):
    X = []
    Y = []
    flag = 0
    prev_key = 0
    for key, value in tw_per_hour.items():
        # print(key, ' feature = ', tw_per_hour[key])   
        if flag != 0:
            X.append(tw_per_hour[prev_key])
            Y.append(tw_per_hour[key][0])
        flag = 1
        prev_key = key
    X = np.array(X)
    Y = np.array(Y)
    result = statapi.OLS(Y, X).fit()
    print(result.summary())

def openHash(filename):
    tw_per_hour = {}
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
    linearReg(tw_per_hour)

if __name__ == "__main__":
    for hashtag in hashtags:
        print("#" + hashtag)
        openHash('tweet_data/tweets_#' + hashtag + '.txt')
