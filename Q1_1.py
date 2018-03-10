import json
import datetime, time
import pytz
import matplotlib.pyplot as plt 

# filenames = ["tweets_#gopatriots.txt"]
filenames = ["tweets_#gohawks.txt", "tweets_#nfl.txt", "tweets_#sb49.txt", "tweets_#gopatriots.txt", "tweets_#patriots.txt", "tweets_#superbowl.txt"]
# filenames = ["tweets_#nfl.txt", "tweets_#superbowl.txt"]
# for fname in filenames: 
#   tw_per_hour = {}
#   followers_num = 0
#   retweets_num = 0
#   line = 0
#   with open("tweet_data/"+fname) as f:
#     tweets = f.readlines()
#     for tw in tweets:
#       line += 1
#       tw = json.loads(tw)
#       citation_date = tw["citation_date"]
#       pst_tz = pytz.timezone('US/Pacific')
#       time_str = datetime.datetime.fromtimestamp(citation_date, pst_tz)
      
#       post_hour = (time_str.month*100 + time_str.day)*100 + time_str.hour
#       # print(time_str, post_hour)
#       if post_hour in tw_per_hour:
#         tw_per_hour[post_hour] += 1
#       else:
#         tw_per_hour[post_hour] = 1
      
#       followers_num += tw['author']['followers']
#       retweets_num += tw['metrics']['citations']['total']

#   # print(tw_per_hour)
#   print("filenames:", fname)
#   print('Avg # of tweets per hour: ', sum([tw_per_hour[i] for i in tw_per_hour])/len(tw_per_hour))
#   print('Avg # of followers: ', followers_num/line)
#   print('Avg # of retweets: ', retweets_num/line)
  
#   print("for checking", sum([tw_per_hour[i] for i in tw_per_hour]), line)
#   print('-'*20)

import collections

for fname in ["tweets_#nfl.txt", "tweets_#superbowl.txt"]: 
  tw_per_hour = {}
  line = 0
  with open("tweet_data/"+fname) as f:
    tweets = f.readlines()
    for tw in tweets:
      line += 1
      tw = json.loads(tw)
      citation_date = tw["citation_date"]
      pst_tz = pytz.timezone('US/Pacific')
      time_str = datetime.datetime.fromtimestamp(citation_date, pst_tz)
      
      post_hour = (time_str.month*100 + time_str.day)*100 + time_str.hour
      # print(time_str, post_hour)
      if post_hour in tw_per_hour:
        tw_per_hour[post_hour] += 1
      else:
        tw_per_hour[post_hour] = 1
      
  # print(tw_per_hour)
  od = collections.OrderedDict(sorted(tw_per_hour.items()))
  x = []
  y = []
  for k, v in od.items(): 
    x.append(k) # hour
    y.append(v) # num of post
  print(y)
  plt.figure()
  plt.hist(y, normed=True)
  plt.ylabel('posts per hour')
  plt.xlabel('hour')
  
  plt.savefig('plot/'+fname+'_per_hour.png')
  plt.clf()