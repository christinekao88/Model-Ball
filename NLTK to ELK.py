import csv
import json
from elasticsearch import Elasticsearch

# create instance of elasticsearch
es = Elasticsearch('http://35.194.191.163:9200')

import os
dir_locate = "/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/re_search_sentiment_v4/" #資料夾目錄
files = os.listdir(dir_locate) # 得到資料夾下的所有檔名稱


for path in files:
    name = path.split('.')[0]
    path_url = "/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/re_search_sentiment_v4/"+path
    print('start..............................................' + path)
    with open( path_url ,  'r', encoding='utf-8') as f:
        try:
            for line in f.readlines():
                data_list = json.loads(line)['data']
                for data in data_list:
                    es.index(index=name+'_sentiment_02',body=data,request_timeout=100000)
                    print(name + '..........continue')
        except UnicodeDecodeError:
            continue
    print(name + '..........finished')

print('Upload Successful!!')



# Create new index
body = {"mappings": {
         "properties": {
             "id": {"type": "integer"},
             "conversation_id": {"type": "integer"},
             "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
             "date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
             "timezone": {"type": "keyword"},
             "place": {"type": "keyword"},
             "location": {"type": "keyword"},
             "tweet": {"type": "text"},
             "clean_tweet": {"type": "text"},
             "hashtags": {"type": "keyword", "normalizer": "hashtag_normalizer"},
             "cashtags": {"type": "keyword", "normalizer": "hashtag_normalizer"},
             "user_id_str": {"type": "keyword"},
             "username": {"type": "keyword", "normalizer": "hashtag_normalizer"},
             "name": {"type": "text"},
             "profile_image_url": {"type": "text"},
             "day": {"type": "integer"},
             "hour": {"type": "integer"},
             "link": {"type": "text"},
             "retweet": {"type": "text"},
             "essid": {"type": "keyword"},
             "nlikes": {"type": "integer"},
             "nreplies": {"type": "integer"},
             "nretweets": {"type": "integer"},
             "quote_url": {"type": "text"},
             "video": {"type": "integer"},
             "search": {"type": "text"},
             "near": {"type": "text"},
             "geo_near": {"type": "geo_point"},
             "geo_tweet": {"type": "geo_point"},
             "photos": {"type": "text"},
             "user_rt_id": {"type": "keyword"},
             "mentions": {"type": "keyword", "normalizer": "hashtag_normalizer"},
             "source": {"type": "keyword"},
             "user_rt": {"type": "keyword"},
             "retweet_id": {"type": "keyword"},
             "reply_to": {
                 "type": "nested",
                 "properties": {
                     "user_id": {"type": "keyword"},
                     "username": {"type": "keyword"}
                 }
             },
             "retweet_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss",
                              "ignore_malformed": True},
             "urls": {"type": "keyword"},
             "translate": {"type": "text"},
             "trans_src": {"type": "keyword"},
             "trans_dest": {"type": "keyword"},
             "Subjectivity": {"type": "float"},
             "Polarity": {"type": "float"},
             "Analysis": {"type": "keyword"},
                     }
                   }
                }
#
#     print('creating '+name+' index.........')
#     try:
#         es.indices.create(index=name+'_v4', body = body)
#     except Elasticsearch.exceptions.RequestError:
#         continue

