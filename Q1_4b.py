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

  for fname in filenames:
    before_X, before_Y, between_X, between_Y, after_X, after_Y = Q1_4.read_data(fname)
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