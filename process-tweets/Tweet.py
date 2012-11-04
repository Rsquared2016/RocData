class Tweet:

    def __init__(self):
        self.userName = None
        self.WRONGuserID = None
        self.msgID = None

        self.location = None
        self.lat = None
        self.lon = None

        self.createdAt = None
	self.datetime = None
        self.text = None

        self.profile_image = None
        self.json = None
        
    def toString(self):
        return "%s @ [%s, %s] on %s says: \"%s\"" % (self.userName, self.lat, self.lon, self.createdAt, self.text.strip())
