from datetime import datetime

class Tweet:
    def __init__(self, tweetID, dt, userID, screen_name, lat, lon, text):
        self.tweetID = tweetID
        self.dt = datetime.strptime(dt, "%m/%d/%Y %I:%M:%S %p")
        self.userID = int(userID)
        self.screen_name = screen_name
        self.lat = float(lat)
        self.lon = float(lon)		
        self.text = text
    
    def __str__(self):
        return '%d %s %.6f %.6f %s' % (self.tweetID, self.dt, self.lat, self.lon, self.text.strip())