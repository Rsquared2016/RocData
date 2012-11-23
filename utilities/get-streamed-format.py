
import tweetstream
import json

username = 'corporaMine'
password = 'tw1tterhea1th'
user_filter = ["807095"]
tweet_stream = tweetstream.FilterStream(username, password, follow=user_filter)
for tweet in tweet_stream:
    print "%s" % json.dumps(tweet, indent=4)
    break
