import json
import datetime, time
import pytz
filenames = ["tweets_#gopatriots.txt"]
# filenames = ["tweets_#gohawks.txt", "tweets_#nfl.txt", "tweets_#sb49.txt", "tweets_#gopatriots.txt", "tweets_#patriots.txt", "tweets_#superbowl.txt"]
# filenames = ["tweets_#nfl.txt", "tweets_#superbowl.txt"]
for fname in filenames: 
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
      print(time_str, post_hour)
      if post_hour in tw_per_hour:
        tw_per_hour[post_hour] += 1
      else:
        tw_per_hour[post_hour] = 1
      
  print(len(tw_per_hour))
  print(sum([tw_per_hour[i] for i in tw_per_hour])/len(tw_per_hour))