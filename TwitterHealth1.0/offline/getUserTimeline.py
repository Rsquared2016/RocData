from twython import Twython
import simplejson as json

numTweetsPerQuery = 15

handleToInfo = {}
fin = open('venueID_twitterHandle.txt', 'r')
for line in fin:
    (venueID, twitterHandle, venueName, venueDesc, venueAddr, venueLat, venueLon, numEvents) = line.split('\t')
    handleToInfo[twitterHandle] = {'id': int(venueID), 'twitterHandle': twitterHandle, 'name': venueName, 'description': venueDesc, 'address': venueAddr, 'lat': float(venueLat), 'lon': float(venueLon), 'numEvents': int(numEvents)}

# We won't authenticate for this, but sometimes it's necessary
twitter = Twython()

venues = []
for twitterHandle in handleToInfo.keys():
    user_timeline = twitter.getUserTimeline(screen_name=twitterHandle, rpp=numTweetsPerQuery)
    search_results = twitter.searchTwitter(q=twitterHandle, rpp=numTweetsPerQuery, lang="en")
    venue = handleToInfo[twitterHandle]
    tweetsTimeline = []
    tweetsSearch = []
    for tweet in user_timeline:
        tweetsTimeline.append(tweet)
    for tweet in search_results["results"]:
        tweetsSearch.append(tweet)
    venue['tweetsTimeline'] = tweetsTimeline
    venue['tweetsSearch'] = tweetsSearch
    venues.append(venue)
    
print json.dumps(venues, sort_keys=True)


