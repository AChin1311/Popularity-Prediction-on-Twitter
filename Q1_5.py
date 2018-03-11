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
test_filenames = ["sample1_period1.txt", "sample2_period2.txt", "sample3_period3.txt", "sample4_period1.txt", "sample5_period1.txt", "sample6_period2.txt", "sample7_period3.txt", "sample9_period2.txt", "sample10_period3.txt"]

def read_test_data(filename):
  tw_per_hour = {}

  with open('test_data/'+filename,'r') as f:
    tweets = f.readlines()

    for tw in tweets:
      tw = json.loads(tw)
      time_str = datetime.fromtimestamp(tw["citation_date"], pst_tz)
      post_hour = (time_str.month * 100 + time_str.day) * 100 + time_str.hour
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
  return seperate_test_data(tw_per_hour)

def seperate_test_data(data, n=5):
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

  before_event_X = [list(itertools.chain.from_iterable(before_event[i-n:i])) for i in range(n, len(before_event))][-1:]
  before_event_Y = [l[0] for l in before_event[n:]][-1:]
  between_event_X = [list(itertools.chain.from_iterable(between_event[i-n:i])) for i in range(n, len(between_event))][-1:]
  between_event_Y = [l[0] for l in between_event[n:]][-1:]
  after_event_X = [list(itertools.chain.from_iterable(after_event[i-n:i])) for i in range(n, len(after_event))][-1:]
  after_event_Y = [l[0] for l in after_event[n:]][-1:]
  
  return before_event_X, before_event_Y, between_event_X, between_event_Y, after_event_X, after_event_Y

def RF_regr(X, Y):
  X = np.array(X)
  Y = np.array(Y)
  regr = RandomForestRegressor(n_estimators=30, n_jobs=-1)
  regr.fit(X, Y)
  return regr

if __name__ == "__main__":

  before_event_X = []
  before_event_Y = []
  between_event_X = [] 
  between_event_Y = []
  after_event_X = []
  after_event_Y = []

  for fname in filenames:
    print(fname)
    before_X, before_Y, between_X, between_Y, after_X, after_Y = Q1_4.read_data(fname)
    before_event_X.extend(before_X)
    before_event_Y.extend(before_Y)
    between_event_X.extend(between_X)
    between_event_Y.extend(between_Y)
    after_event_X.extend(after_X)
    after_event_Y.extend(after_Y)

  
  for test_fname in test_filenames:
    print(test_fname)
    before_test_X, before_test_Y, between_test_X, between_test_Y, after_test_X, after_test_Y = read_test_data(test_fname)
    print(len(before_test_X), len(before_test_Y), len(between_test_X), len(between_test_Y), len(after_test_X), len(after_test_Y))

    print("random forest regression:")

    if "period1" in test_fname:
      print("before event")
      regr = RF_regr(before_event_X, before_event_Y)
      Y_predict = regr.predict(before_test_X)
      test_error = abs(before_test_Y[0] - Y_predict[0])
      print("Mean Absolute Error: ", test_error)

    elif "period2" in test_fname:
      print("between event")
      regr = RF_regr(between_event_X, between_event_Y)
      Y_predict = regr.predict(between_test_X)
      test_error = abs(between_test_Y[0] - Y_predict[0])
      print("Mean Absolute Error: ", test_error)

    elif "period3" in test_fname:
      print("after event")
      regr = RF_regr(after_event_X, after_event_Y)
      Y_predict = regr.predict(after_test_X)
      test_error = abs(after_test_Y[0] - Y_predict[0])
      print("Mean Absolute Error: ", test_error)

    print('-'*20)
