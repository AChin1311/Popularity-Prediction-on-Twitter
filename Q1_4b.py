import json
from datetime import datetime
import pytz
import collections
import statsmodels.api as statapi
import itertools
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold
import numpy as np
import Q1_4

pst_tz = pytz.timezone('US/Pacific') 
filenames = ["tweets_#gohawks.txt", "tweets_#nfl.txt", "tweets_#sb49.txt", "tweets_#gopatriots.txt", "tweets_#patriots.txt", "tweets_#superbowl.txt"]
# filenames = ["tweets_#gohawks.txt"]

def read_all_data(fname, fid):
  tw_per_hour = {}
  for i in range(14, 32):
    for j in range(24):
      hr_str = 10000+(i)*100+j
      tw_per_hour[hr_str] = [0, 0, 0, 0, j, fid]

  for i in range(7): 
    for j in range(24):
      if i == 6 and j == 11:
        break
      hr_str = 20000+(i+1)*100+j
      tw_per_hour[hr_str] = [0, 0, 0, 0, j, fid]


  with open("tweet_data/"+fname,'r') as f:
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
      
    f.close()

  tw_per_hour = collections.OrderedDict(sorted(tw_per_hour.items()))
  return seperate_data(tw_per_hour)

def seperate_data(data, n=5):
  before_event = []
  between_event = []
  after_event = []
  
  for k,v in data.items():
    if k < 20108:
      before_event.append(v)
    elif k >= 20108 and k <= 20120:
      between_event.append(v)
    elif k > 20120:
      after_event.append(v)

  
  before_event_X = [list(itertools.chain.from_iterable(before_event[i-n:i])) for i in range(n, len(before_event))]
  before_event_Y = [l[0] for l in before_event[n:]]

  between_event_Y = [l[0] for l in between_event]
  between_event = before_event[-5:]+between_event
  between_event_X = [list(itertools.chain.from_iterable(between_event[i:i+n])) for i in range(0, len(between_event)-n)]
  
  after_event_Y = [l[0] for l in after_event]
  after_event = between_event[-5:]+after_event
  after_event_X = [list(itertools.chain.from_iterable(after_event[i:i+n])) for i in range(0, len(after_event)-n)]
  
  return before_event_X, before_event_Y, between_event_X, between_event_Y, after_event_X, after_event_Y



def linear_regr(X, Y):
  X = np.array(X)
  Y = np.array(Y)
  regr = statapi.OLS(Y, X).fit()
  Y_predict = regr.predict(X)
  test_error = mean_absolute_error(Y, Y_predict)
  print("Mean Absolute Error: ", np.mean(test_error))


def kNN_regr(X, Y):
  X = np.array(X)
  Y = np.array(Y)
  regr = KNeighborsRegressor(n_neighbors = min(10,len(Y)-1), n_jobs=-1)
  regr.fit(X, Y)
  Y_predict = regr.predict(X)
  test_error = mean_absolute_error(Y, Y_predict)
  print("Mean Absolute Error: ", np.mean(test_error))

def RF_regr(X, Y):
  X = np.array(X)
  Y = np.array(Y)
  regr = RandomForestRegressor(n_estimators=30, n_jobs=-1)
  regr.fit(X, Y)
  Y_predict = regr.predict(X)
  test_error = mean_absolute_error(Y, Y_predict)
  print("Mean Absolute Error: ", np.mean(test_error))

if __name__ == "__main__":

  before_event_X = []
  before_event_Y = []
  between_event_X = [] 
  between_event_Y = []
  after_event_X = []
  after_event_Y = []

  for i, fname in enumerate(filenames):
    print("reading file ", fname)
    before_X, before_Y, between_X, between_Y, after_X, after_Y = read_all_data(fname, i)
    print(len(before_X), len(between_X), len(after_X))
    print(len(before_Y), len(between_Y), len(after_Y))
    before_event_X.extend(before_X)
    before_event_Y.extend(before_Y)
    between_event_X.extend(between_X) 
    between_event_Y.extend(between_Y)
    after_event_X.extend(after_X)
    after_event_Y.extend(after_Y)
    

  print("random forest regression:")
  print("before event")
  RF_regr(before_event_X, before_event_Y)
  print("between event")
  RF_regr(between_event_X, between_event_Y)
  print("after event")
  RF_regr(after_event_X, after_event_Y)
  print('-'*20)
  print('-'*20)