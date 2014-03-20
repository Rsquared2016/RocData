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

client = Twitter::REST::Client.new do |config|
  config.consumer_key        = consumer_key
  config.consumer_secret     = consumer_secret
  config.access_token        = access_token
  config.access_token_secret = access_token_secret
end


def crawl_graph(client, user, iteration, total)
  if iteration < total 
    client.friends(user).take(200).each do |follower|
      store_in_db('social_graph.txt', "  #{user} --- #{follower.screen_name};\n") 
      crawl_graph(client, follower.screen_name, (iteration+1) , total)
    end
  end
end

store_in_db('social_graph.txt',"graph relations { \n")
crawl_graph(client, 'androwis', 0, 2)
store_in_db('social_graph.txt',"} \n")
