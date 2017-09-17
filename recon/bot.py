import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API 

from pattern.en import sentiment
from nltk.chat import eliza

chatbot = eliza.Chat(eliza.pairs)

with open('config.json') as data_file: settings = json.load(data_file)

consumer_key = settings['twitter']['consumer_key']
consumer_secret = settings['twitter']['consumer_secret']
access_key = settings['twitter']['access_token_key']
access_secret = settings['twitter']['access_token_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
twitter = API(auth)

screen_name = 'nthcolumn'
account_user_id = twitter.get_user(screen_name=screen_name)

class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            chatResponse = chatbot.respond(tweetText)

            replyText = '@' + screenName + ' ' + chatResponse

            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            # If rate limited, the status posts should be queued up and sent on an interval
            twitter.update_status(status=replyText, in_reply_to_status_id=tweetId)

    def on_error(self, status):
        print status


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
