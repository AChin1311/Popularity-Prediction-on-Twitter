import json
import datetime, time
import pytz

filenames = ["tweets_#gohawks.txt", "tweets_#gopatriots.txt", "tweets_#nfl.txt", "tweets_#patriots.txt", "tweets_#sb49.txt", "tweets_#superbowl.txt"]
for fname in filenames: 
  with open("tweet_data/"+fname) as f:
    tweets = f.readlines()
    for tw in tweets:
      tw = json.loads(tw)
      print(tw["firstpost_date"])


  # pst tz = pytz.timezone(’US/Pacific’)
  # datetime.datetime.fromtimestamp(citation date, pst tz)