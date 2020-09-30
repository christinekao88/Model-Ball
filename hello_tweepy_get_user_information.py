import csv
import pandas as pd
import tweepy
import numpy
# twitter提供的開發Key和secret Key:存放至credentials,並匯入使用
import credentials as c
from datetime import datetime
auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
auth.set_access_token(c.access_token, c.access_token_secret)
api = tweepy.API(auth)

def user_informadtion(id):
    user = api.get_user(id)
    print('User Screen Name: ' + user.screen_name)
    print('User Name: ' + user.name)
    print('User ID: ' + user.id_str)
    print('Location : ' + user.location)
    print('Description : ' + user.description)
    print('How many tweets : ' + str(user.statuses_count))
    print('Url : ' + user.url)
    print('How many followers : '+str(user.followers_count))
    print('How many friends : '+str(user.friends_count))
    for friend in user.friends():
        print('Following : '+friend.screen_name)



def user_status(id):
    tweet = tweepy.Cursor(api.user_timeline, id).items(200)
    tweets=[]
    retweets=[]
    for status in tweet:
        # print(status._json)

        if 'RT' in status.text.split('@')[0]:
            # print('============= Retweet ================')
            date = status._json['created_at'].replace('+0000 ', '')
            date_format = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
            # print('User retweet at: ' + str(date_format))
            retweets.append(str(date_format))

            # tweet本身的id in user region
            id_str = status._json['id_str']
            # print('This tweet\'s ID in user timeline: ' + id_str)
            retweets.append(id_str)

            # Tweet text(not complete)
            # content = status.text.split(':')[1]
            # print('Tweet\'s content:'+ content)

            author = dict(status._json['entities']['user_mentions'][0])
            author_screen_name = author['screen_name']
            # print('Author\'s screen name:' + author_screen_name)
            retweets.append(author_screen_name)

            id_str = author['id_str']
            # print('Author\'s id:' + id_str)
            retweets.append(id_str)

            user_follow = status._json['source'].split('"')[3]
            # print('Does user follow author : '+user_follow)
            retweets.append(user_follow)

            # in_reply_to_status_id_str = status._json['in_reply_to_status_id_str']
            # print('in_reply_to_status_id_str : '+str(in_reply_to_status_id_str))
            #
            # in_reply_to_user_id_str = status._json['in_reply_to_user_id_str']
            # print('in_reply_to_user_id_str : '+str(in_reply_to_user_id_str))
            #
            # in_reply_to_screen_name = status._json['in_reply_to_screen_name']
            # print('in_reply_to_screen_name : '+str(in_reply_to_screen_name))

            retweet_sataus = status._json['retweeted_status']
            # print(retweet_sataus)
            retweet_at = retweet_sataus['created_at'].replace('+0000 ', '')
            retweet_at_format = datetime.strptime(retweet_at, "%a %b %d %H:%M:%S %Y")
            # print('Tweet is created at: ' + str(retweet_at_format))
            retweets.append(retweet_at)

            retweet_id_str = retweet_sataus['id_str']
            # print('Retweet\'s Text\'s ID: ' + retweet_id_str)
            retweets.append(retweet_id_str)

            retweet_content = retweet_sataus['text']
            # print('Retweet\'s content: ' + retweet_content)
            retweets.append(retweet_content)

            retweet_truncated = retweet_sataus['truncated']
            # print('Is retweet be truncated : ' + str(retweet_truncated))
            retweets.append(retweet_truncated )

            # how many times this Tweet has been liked by Twitter users
            favorite_count = retweet_sataus['favorite_count']
            # print('How many likes : ' + str(favorite_count))
            retweets.append(favorite_count)

            # Number of times this Tweet has been retweeted
            retweet_count = retweet_sataus['retweet_count']
            # print('How many retweets : ' + str(retweet_count))
            retweets.append(retweet_count)

        else:

            # print('============= User Tweet ================')
            # when this Tweet was created
            date = status._json['created_at'].replace('+0000 ', '')
            date_format = datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
            # print('User tweet at: ' + str(date_format))
            tweets.append(str(date_format))


            # tweet本身的id in user region
            id_str = status._json['id_str']
            # print('This tweet\'s ID : ' + id_str)
            tweets.append(id_str)

            # Tweet text
            content = status.text
            # print('Tweet\'s content:'+ content)
            tweets.append(content)

            truncated = status._json['truncated']
            # print('Is tweet be truncated : ' + str(truncated))
            tweets.append(truncated)

            # Number of times this Tweet has been retweeted
            retweet_count = status._json['retweet_count']
            # print('How many retweets : ' + str(retweet_count))
            tweets.append(retweet_count)

            # how many times this Tweet has been liked by Twitter users
            favorite_count = status._json['favorite_count']
            # print('How many likes : ' + str(favorite_count))
            tweets.append(favorite_count)


            # # Number of times this Tweet has been replied to
            # reply_count= status._json['reply_count']
            # print('How many replies : ' + str(reply_count))

            # if reply_count >0:
            #     #  the screen name of the original Tweet’s author.
            #
            #     in_reply_to_screen_name = status._json['in_reply_to_screen_name']
            #     print('Relpy by: @'+in_reply_to_screen_name)
            #
            #     # If Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID. Example:
            #     in_reply_to_status_id_str = status._json['in_reply_to_status_id_str']
            #     print(' The original Tweet’s ID: '+in_reply_to_status_id_str)
            #
            #     # If the represented Tweet is a reply, this field will contain the string representation of the original Tweet’s author ID
            #     in_reply_to_user_id_str=status._json['in_reply_to_user_id_str']
            #     print(' The original Tweet’s author ID: '+in_reply_to_user_id_str)
            #
            #
            #  # Indicates approximately how many times this Tweet has been quoted by Twitter users
            # quote_count= status._json['quote_count']
            # if status._json['is_quote_status']=='true':
            #     print('How many replies : ' + str(quote_count))

            # transform the tweepy tweets into a 2D array that will populate the csv
            # outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

    size_tweets=int(numpy.size(tweets)/6)
    tweets_array=numpy.array(tweets).reshape(size_tweets,6)
    # It is now possible to convert tweets_data to a pandas DataFrame with the tweets_data list.
    df_tweet = pd.DataFrame(tweets_array, columns=['user_created_at', 'This tweet\'s ID', 'text', 'Is tweet be truncated','retweet_count','favorite_count'])
    # 顯示所有列
    pd.set_option('display.max_columns', None)
    # 顯示所有行
    pd.set_option('display.max_rows', None)
    # 設置顯示的寬度為2000，防止輸出內容被換行
    pd.set_option('display.width', 2000)
    print(df_tweet.head())
    user = api.get_user(id)
    df_tweet.to_csv(user.screen_name+'.csv')

    size_retweets = int(numpy.size(retweets) / 11)
    retweets_array=numpy.array(retweets).reshape(size_retweets,11)
    # print(retweets_array)
    df_retweet = pd.DataFrame(retweets_array, columns=['User retweet at', 'tweet\'s ID in user timeline','Author\'s screen name', 'Author\'s id:','user follow author ',' created at','Retweet\'s Text\'s ID: ','Retweet\'s content: ', 'Is tweet be truncated','retweet_count','favorite_count'])
    print(df_retweet.head())


    # # write the csv
    # user = api.get_user(id)
    # screen_name = user.screen_name
    # with open(f'{screen_name}_tweets.csv', 'w',newline ='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["id", "created_at", "text"])
    #     for row in tweets:
    #         writer.writerows(row)
    #     for row_r in retweets:
    #         writer.writerows(row_r)

# newline='' 參數，這是為了讓資料中包含的換行字元可以正確被解析
# with open ('ID_reference.csv_','r',newline='') as csvfile:
#     # 讀取 CSV 檔案內容
#     # reader = csv.reader(csvfile)
#     reader = csv.DictReader(csvfile)
#     column = [row['mlb_name'] for row in reader]
#     # print(column) #list







# user_informadtion(133880286)
user_status(133880286)

