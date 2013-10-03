// List
// ----------------
// handler for the list view

define(["controls", "text!/resources/templates/mobile/list-view.html",
        "text!/resources/templates/mobile/tweet-view.html"], function(Controls,
    listView, tweetView) {
    // Constructor
    list = function(model) {
        var self = this;
        this.model = model;
        this.html = null;
        this.controls = {
            ratingPanels: {}
        }
    };
    
    // Instance Methods
    list.prototype = {
        init: function() {
            var self = this;
            var user_id = self.model.map.user_id;
            this.html = _.template(listView, this.model);
            $(".mobile-body").append(this.html);
            $.each(this.model.tweets, function(index, tweet) {
                var html = _.template(tweetView, { tweet: tweet });
                $('.list-view').append(html);
                // create buttons for rating tweet accuracy
                self.controls.ratingPanels[tweet._id] = {};
                // rate buttons click handler
                var that = this;
                $('#' + tweet._id + ' .feedback-button').each(function(){
                    $(this).click(function(){
                        var tweet_id = $(this).parents('.list-view-tweet').attr('id');
                        _.setButtonAsActive($(this));
                        console.log('TODO check values sent to server');
                        tweet.update({
                            feedback: {
                                user_id: user_id,
                                rating: _.tweetRating($(this).attr('class')),
                                time: _.currentTimeAsTwitterFormat()
                            }
                        });
                    });
                });

                // display feedback time and
                // make selected button somewhat transparent
                if(tweet.hasRating(user_id)) {
                    var ftime = tweet.getFeedback(user_id).time;
                    var date = _.twitterFormatToDate(ftime);
                    var timeSimple = _.dateToSimple(date);
                    $('.list-view #' + tweet._id + ' .tweet-rating').children('span')
                        .text('Last rated on ' + timeSimple.split(/\s/g)[0]);
                    
                    if(tweet.getRating(user_id) > 0) {
                        _.setButtonAsActive($("#" + tweet._id + " .yes_button"));
                    } else if(tweet.getRating(user_id) < 0) {
                        _.setButtonAsActive($("#" + tweet._id + " .no_button"));
                    } else {
                        _.setButtonAsActive($("#" + tweet._id + " .maybe_button"));
                    }
                }
            });
        },

        destroy: function() {
            this.html = '';
            $("#list").remove();
        },
        
        show: function() {
            if (!this.html)
                this.init();
            $('.mobile-body .list-view').show();
            $('#map_overlay_tweet_wrapper').hide();
            
            var model = this.model;
            model.map.hide();
            _.setLinkWithIcon($('a#view_toggle_link'), 'Map', 'icon-map-marker');
            $('a#view_toggle_link').unbind('click').bind('click', function(){
                model.map.show();
            });
        },
        
        hide: function() {
            $('.mobile-body .list-view').hide();
        }
    };
    
    return list;
});
