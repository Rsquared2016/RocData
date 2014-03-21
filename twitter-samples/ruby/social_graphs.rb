gem 'twitter'
require 'twitter'
require 'set'
require 'colorize'

# See https://github.com/sferik/twitter for more documentation.

###############################################################################
#
# Include your own credentials here.
# https://dev.twitter.com/docs/faq
# --> See how to obtain an API Key
#
  @consumer_key        = "W7MMNcGAPTOrbhiQAP9r2Q"
  @consumer_secret     = "g6ds0f5OB1LfsLDo5I1UMyrTvF32IoQwHKXKqFj0P6U"
  @access_token        = "1223199230-4cEZSklxH3b3ME9QEwBC3h4K3VZ18MhlSvSvZnA"
  @access_token_secret = "jDTwCY3yCY9nviqKMq2GGV1L2BH89RZhhgmx7v4Imiy5E"

  users = Hash.new(0)


def store_in_db(filename, str)
    filename.puts(str)
end
def twitter_client
   Twitter::REST::Client.new do |config|
    config.consumer_key        = @consumer_key
    config.consumer_secret     = @consumer_secret
    config.access_token        = @access_token
    config.access_token_secret = @access_token_secret
  end
end

def fetch_all_friends(db, twitter_username, degree, max_attempts = 100)
  num_attempts = 0
  new_users = Hash.new(0)
  client = twitter_client
  myfile = File.new("#{twitter_username}_friends_list.txt", "w")
  running_count = 0
  cursor = -1
  while (cursor != 0) do
    begin
      num_attempts += 1
      # 200 is max, see https://dev.twitter.com/docs/api/1.1/get/friends/list
      friends = client.friends(twitter_username, {:cursor => cursor, :count => 200} )
      friends.each do |f|
        running_count += 1
        new_users[f.screen_name] = degree+1
        store_in_db(db, "  #{twitter_username} -- #{f.screen_name};\n")
        myfile.puts "\"#{running_count}\",\"#{f.name.gsub('"','\"')}\",\"#{f.screen_name}\",\"#{f.url}\",\"#{f.followers_count}\",\"#{f.location.gsub('"','\"').gsub(/[\n\r]/," ")}\",\"#{f.created_at}\",\"#{f.description.gsub('"','\"').gsub(/[\n\r]/," ")}\",\"#{f.lang}\",\"#{f.time_zone}\",\"#{f.verified}\",\"#{f.profile_image_url}\",\"#{f.website}\",\"#{f.statuses_count}\",\"#{f.profile_background_image_url}\",\"#{f.profile_banner_url}\""
      end
      return new_users if not friends.respond_to? :next_cursor
      cursor = friends.next_cursor
      return new_users if cursor == 0
    rescue Twitter::Error::TooManyRequests => error
      if num_attempts <= max_attempts
        if friends != nil
          return new_users if not friends.respond_to? :next_cursor
          cursor = friends.next_cursor
          cursor = friends.next_cursor if friends && friends.next_cursor
        end
        time = 5* (error.rate_limit.reset_in + num_attempts)
        print "Hit rate limit on #{twitter_username}, sleeping for #{time} seconds | ".red
        time.times{sleep 1; print "."}
        print "\n"
        retry
      else
        raise
      end
    end
  end
end


def crawl_graph(db, users, total)
  new_users = Hash.new(0)
  users.each do |user|
    if user[1] < total
      new_users.merge!(fetch_all_friends(db, user[0], user[1]))
    end
  end
  puts new_users
  crawl_graph(db, new_users, total) if new_users.size > 0
end


db = File.new("androwis_social_graph.txt", "w")
store_in_db(db,"graph relations { \n")
users["androwis"] = 0
crawl_graph(db, users, 2)
store_in_db(db,"} \n")
