import tweepy
# twitter提供的開發Key和secret Key:存放至credentials,並匯入使用
import credentials as c

# Using the keys, setup the authorization
auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
auth.set_access_token(c.access_token, c.access_token_secret)

# Create the API object
# The API class provides access to the entire twitter RESTful API methods
api = tweepy.API(auth)


""" TIMELINE()"""
# 自己主頁上的時間軸里的内容
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

# 其他用户主頁上的時間軸里的内容
public_tweets = api.user_timeline('LeoDiCaprio')
for tweet in public_tweets:
    print(tweet.text)

"""Get the User object for twitter user"""
# Models:When we invoke an API method most of the time returned back to us will be a Tweepy model class instance
user = api.get_user('LeoDiCaprio')
#
# # Models contain the data and some helper methods which we can then use:
# # 取得user的 @ screen_name
# print(user.screen_name)
# # 有多少追蹤者 Follower
print(user.followers_count)
# # 詳列出Following的帳號
# for friend in user.friends():
#     print(friend.screen_name)



# How to text tweet : 發文在自己的頁面上
# api.update_status("Tweet using #tweepy")

# How to media tweet : 發照片
# image = os.environ['USERPROFILE'] + "\\Pictures\\cubes.jpg"
# api.update_with_media(image, "Tweet with media using #tweepy")
# return a status object with a lot of useful data

# How to reply to a tweet : you'd first need its tweet_id
# which you can get from the tweet's URL.
# https://twitter.com/KAO79922715/status/1259863107347689472
# id_of_tweet_to_reply = "1259863107347689472"
# twitter.update_status("Reply to a tweet using #tweepy", in_reply_to_status_id=id_of_tweet_to_reply)




"""" Tweepy has the Cursor object:To help make pagination easier and require less code
     api.user_timeline(id="twitter") or
     api.Cursor(api.user_timeline, id="twitter")"""

# search:tweepy
# for tweet in api.Cursor(api.search, q='tweepy').items(10):
#     print(tweet.text)
# 搜索具有League of Legends(lol英雄联盟的全称)的关键词的帐号
# for tweet in api.Cursor(twitter.search,q='League of Legends').items(10):
#     print('Tweet by: @' + tweet.user.screen_name)

# Iterate through the first 200 statuses in the home timeline
# for status in api.Cursor(api.user_timeline).items(200):
    # Process the status here
    # print(status._json)
    # the text attribute of Status objects returned text
    # print(status.text)

# Only iterate through the first 3 pages
# for page in tweepy.Cursor(api.user_timeline).pages(3):
#     # page is a list of statuses
#     print(page)


# FollowAll : follow every follower of the authenticated user.
# for follower in api.Cursor(api.followers).items():
#     follower.follow()


# to print the full text of the Tweet, or if it’s a Retweet,
#  the full text of the Retweeted Tweet:

status = api.get_status(id, tweet_mode="extended")
try:
    print(status.retweeted_status.full_text)
except AttributeError:
    # Not a Retweet
    print(status.full_text)

def on_status(self, status):
    # Check if Retweet
    # If status is a Retweet, it will not have an extended_tweet attribute,
    # and status.text could be truncated.
    if hasattr(status, "retweeted_status"):
        try:
            print(status.retweeted_status.extended_tweet["full_text"])
        except AttributeError:
            print(status.retweeted_status.text)
    else:
        try:
            print(status.extended_tweet["full_text"])
        except AttributeError:
            print(status.text)


