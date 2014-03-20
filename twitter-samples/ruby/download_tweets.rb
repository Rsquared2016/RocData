gem 'twitter'
require 'twitter'
require 'set'

# See https://github.com/sferik/twitter for more documentation.

###############################################################################
# 
# Include your own credentials here.  
# https://dev.twitter.com/docs/faq
# --> See how to obtain an API Key
#
  consumer_key        = "W7MMNcGAPTOrbhiQAP9r2Q"
  consumer_secret     = "g6ds0f5OB1LfsLDo5I1UMyrTvF32IoQwHKXKqFj0P6U"
  access_token        = "1223199230-4cEZSklxH3b3ME9QEwBC3h4K3VZ18MhlSvSvZnA"
  access_token_secret = "jDTwCY3yCY9nviqKMq2GGV1L2BH89RZhhgmx7v4Imiy5E"

  words = Hash.new(0)


def store_in_db(filename, str)
    File.write(filename, str, File.size(filename), mode:'a')
end

# An example that uses twitter client.
client = Twitter::REST::Client.new do |config|
  config.consumer_key        = consumer_key
  config.consumer_secret     = consumer_secret
  config.access_token        = access_token
  config.access_token_secret = access_token_secret
end

j = 0
client.search("to:justinbieber marry me", :result_type => "recent").collect do |tweet|
  puts "Handling searched tweet #{j}"
  j = j+1
  store_in_db('client_data.txt', "#{tweet.user.screen_name}: #{tweet.text}\n")  
end

# An example that uses twitter streams.
stream = Twitter::Streaming::Client.new do |config|
  config.consumer_key        = consumer_key
  config.consumer_secret     = consumer_secret
  config.access_token        = access_token
  config.access_token_secret = access_token_secret
end

i = 0 
stream.user do |object|
  case object
  when Twitter::Tweet
    puts "Handling streamed tweet #{i}/10"
    store_in_db('streaming_data.txt', "#{object.id} #{object.text.gsub("\n",'')} \n")
    i= i + 1
    if(i > 10)
      return
    end
  when Twitter::DirectMessage
    puts "It's a direct message!"
  when Twitter::Streaming::StallWarning
    warn "Falling behind!"
  end
end
