import json
from datetime import datetime
import pytz
import collections

pst_tz = pytz.timezone('US/Pacific') 
hashtags = ['gohawks' 
            # ,'gopatriots'
            # ,'nfl'
            # ,'patriots'
            # ,'sb49'
            # ,'superbowl'
            ]

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
    for key, value in tw_per_hour.items():
        print(key, ' feature = ', tw_per_hour[key])

if __name__ == "__main__":
    for hashtag in hashtags:
        print("#" + hashtag)
        openHash('tweet_data/tweets_#' + hashtag + '.txt')