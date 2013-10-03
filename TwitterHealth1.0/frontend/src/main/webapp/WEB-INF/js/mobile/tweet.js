// Tweet(s)
// ----------------
// model and logic for a tweet

define(["list", "text!/resources/templates/mobile/tweet-modal.html"], function(List, tweetModal) {
    // Tweet - holds data and overlay for a tweet
    // Constructor
    tweet = function(map, attr) {
        var self = this;
        this._id = attr._id || '';
        this._rev = attr._rev || '';
        this.id_str = attr.id_str;
        this.map = map;
        this.text = attr.text;
        this.from_user = attr.from_user;
        this.location = _.coordinatesToLatLng(attr.geo.coordinates);
        this.created_at = attr.created_at;
        this.health = attr.health;
        this.profile_image = attr.profile_image_url;
        this.feedback = attr.feedback || [];
        if(this.location) {
            this.marker = new google.maps.Marker({
                position: this.location,
                map: this.map.gmap,
                optimized: false,
                icon: {
                    anchor: new google.maps.Point(15,15),
                    url: _.imageForHealth(this.health),
                    scaledSize: new google.maps.Size(29, 31)
                }
            });
        }
        // save the other attributes, why not?
        this.attr = attr;
        google.maps.event.addListener(this.marker, 'click', function(){
            self.clicked();
        });
    };
    
    // Instance Methods
    tweet.prototype = {
        // update
        update: function(attr) {
            if (attr.feedback) {
                this.rate(attr.feedback);
                // save new feedback info
                this.save(attr.feedback, function(data, status) {
                    // make sure we get a success response
                    log.info(data);
                });
            }
        },
        
        // destroy: remove from map
        destroy: function() {
            if(this.marker)
                this.marker.setMap(null);
        },
        
        // save: persist this to the database
        save: function(data, fn) {
            var url = '/m/data/' + this._id + '?lat=' + this.location.lat()
                + '&lng=' + this.location.lng();
            
            $.ajax({
                url: url,
                type: "POST",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "text/plain",
                async: true,
                success: fn
            });
        },
        
        // click: clicked event handler
        clicked: function() {
            console.log(this);
            var tweet = this;
            var user_id = this.map.user_id;
            var html = _.template(tweetModal, {tweet: tweet})
            $('.modal').on('shown', function(){
                $('.modal-feedback-button').each(function(){
                    $(this).click(function(){
                        var tweet_id = $(this).parents('.modal-tweet-response').parent().attr('id').replace("modal_","");
                        _.setButtonAsActive($(this));
                        console.log('TODO send message to server');
                        tweet.update({
                            feedback: {
                            	user_id: user_id,
                            	rating: _.tweetRating($(this).attr('class')),
                                time: _.currentTimeAsTwitterFormat()
                            }
                        });
                    });
                });
            });
            $('.modal').html(html).modal();
        },
        
        getFeedback: function(id) {
            return _.find(this.feedback, function(entry) {
                return entry.user_id == id;
            });
        },
        
        getRating: function(id) {
            return this.getFeedback(id).rating;
        },
        
        rate: function(feedback) {
            this.feedback = _.reject(this.feedback, function(entry) {
                return entry.user_id == feedback.user_id;
            });
            this.feedback.push(feedback);
        },
        
        hasRating: function(id) {
            // true if there's a rating with this user ID
            return _.any(this.feedback, function(entry) {
                log.info(entry.user_id);
                log.info(id);
                log.info((entry.user_id == id) + "");
                return entry.user_id == id;
            });
        },
    };
    
    // Tweets - collection class for tweets
    // Constructor
    tweets = function(map) {
        this.map = map;
        this.all = [];
    };
    
    // Instance Methods
    tweets.prototype = {
        add: function(t) {
            this.all.push(new tweet(this.map, t));
        },
        
        addAll: function(data) {
            var self = this;
            $.each(data, function(index, t) {
                self.add(t);
            });
        },
        
        // each: perform some arbitrary action on all tweets
        each: function(fn) {
            $.each(this.all, fn);
        },
        
        // fetchByGeo: retrieve data from API according to a bounding box
        fetchByGeo: function(l, b, r, t, ulat, ulon, fn) {
            var url = "/m/data/?left=" + l + "&bottom=" + b + "&right=" + r + "&top=" + t;
            if (ulat && ulon)
                url += "&user_lat=" + ulat + "&user_lon=" + ulon;
            $.getJSON(url, fn);
        },
        
        // fetchByGeoAndHealth: in case we want to add that health param in
        // future
        fetchByGeoAndHealth: function(l, b, r, t, ulat, ulon, h, fn) {
            var url = "/m/data/?left=" + l + "&bottom=" + b + "&right=" + r + "&top=" + t
                + "&health=" + h;
            if (ulat && ulon)
                url += "&user_lat=" + ulat + "&user_lon=" + ulon;
            $.getJSON(url, fn);
        },
        
        removeAll: function() {
            $.each(this.all, function(index, t) {
                t.destroy();
            });
            // clear out array
            this.all.length = 0;
        },
        
        sort: function(fn) {
            this.all = _.sortBy(this.all, fn);
        },
        
        sortByHealth: function() {
            this.sort(function(tweet) {
                return tweet.health * -1;
            });
        },
        
        sortByTime: function() {
            this.sort(function(tweet) {
                return new Date(tweet.created_at).getTime() * -1;
            });
        },
        
        size: function() {
            return this.all.length;
        }
    };
    
    return {
        Model: tweet,
        Collection: tweets
    };
});
