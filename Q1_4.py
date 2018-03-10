import json
from datetime import datetime
import pytz
import collections
import itertools

pst_tz = pytz.timezone('US/Pacific') 
# filenames = ["tweets_#gohawks.txt", "tweets_#nfl.txt", "tweets_#sb49.txt", "tweets_#gopatriots.txt", "tweets_#patriots.txt", "tweets_#superbowl.txt"]
filenames = ["tweets_#gohawks.txt"]

def read_data(filename):
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

  with open("tweet_data/"+filename,'r') as f:
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
  before_event_Y = before_event[n:][0]
  between_event_X = [list(itertools.chain.from_iterable(between_event[i-n:i])) for i in range(n, len(between_event))]
  between_event_Y = between_event[n:][0]
  after_event_X = [list(itertools.chain.from_iterable(after_event[i-n:i])) for i in range(n, len(after_event))]
  after_event_Y = after_event[n:][0]
  
  return before_event_X, before_event_Y, between_event_X, between_event_Y, after_event_X, after_event_Y


if __name__ == "__main__":
  for fname in filenames:
    before_event_X, before_event_Y, between_event_X, between_event_Y, after_event_X, after_event_Y = read_data(fname)
    print(before_event_X[:2])
    print(before_event_Y[:2])
    