import json
import markovify
import random
import pattern

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API

consumer_key = 'Ny0rCPUjycgmHMMAKxuKYqs3g'
consumer_secret = 'Cvqf9XQ54KERPhd00zGAXUmlfKL7MIklCWJY9mp7z3pj9U1d3R'
access_token = '912449359891111936-8nerJHp5IcDrVh90Xwkfv4aMKJg9neR'
access_secret = 'Z79dKfUTfUMOjCCk3mkakAauJEk5vycBelDgy9hT77N3w'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter = API(auth, wait_on_rate_limit=True)

## Create bot personality
def bot(nick, text=None):
    if text is None:
        tweets = twitter.user_timeline(nick)
        for i in range(35): 
            tweets += twitter.user_timeline(nick, count=100, max_id=tweets[-1].id)
            
        statuses = [tweet.text.encode("ascii", 'ignore') for tweet in tweets]
        text = ' '.join(statuses)
    bot = markovify.Text(text)
    bot.blurt = bot.make_short_sentence
    return bot
    

realDonaldTrump = bot('realDonaldTrump')

## Setup watch list
dotards = ['@JacobAWohl','@ColinRugg','@OfficeOfMike','@ron8072','@EricaRN4USA','@brawnypatriot','@OpinionOnion7','@Smokes_Angel','@tia6sc']

others = ['@KellyannePolls','@sara_kareena','@RealJamesWoods','@missacarter1','@KlayVolk','@6ee__','@Cassiel_Angelos','@EricRWeinstein','@FreeDailyVideo','@dylansprouse','@DerekUtleyCEO','@HMonfrida','@DonaldJTrumpJr']
print dotards


class ReplyToTweet(StreamListener):

    def on_data(self, data):
        #print data
        tweet = json.loads(data.strip())
        screenName = tweet.get('user',{}).get('screen_name')
        print ("@"+screenName).lower() 
        if ("@"+screenName).lower() in ' '.join(dotards).lower():

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            chatResponse = realDonaldTrump.make_short_sentence(100)+' '+(' '.join(random.sample(dotards, 3)))

            replyText = '@' + screenName + ' ' + chatResponse

            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:139] + ' '

            print('ID    : ' + tweetId)
            print('From  : ' + screenName)
            print('Tweet : ' + tweetText)
            print('Reply : ' + replyText)

            ## Send retweet
            #twitter.update_status(status=replyText, in_reply_to_status_id=tweetId)
            #print replyText
            
    def on_error(self, status):
        print status

if __name__ == '__main__':
    print 'Ooo ra'
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    #twitterStream.userstream(_with='user')
    twitterStream.filter(track=dotards, languages=['en'])
