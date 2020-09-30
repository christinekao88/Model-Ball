import csv
import json
from elasticsearch import Elasticsearch
from datetime import datetime
import pandas as pd
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
# create instance of elasticsearch
es = Elasticsearch('http://35.194.191.163:9200')
# # step 1 : mapping
# mapping = {
#         "mappings": {
#             "properties": {
#                 "date": {
#                     "type": "date"
#                 },
#                 "timestamp_ms": {
#                     "type": "date"
#                 },
#                 "text": {
#                     "type": "text"
#                 },
#                 "location": {
#                     "type": "geo_point"
#                 }
#             }
#         }
#     }
#
# es.indices.create(index='mlb_map', body=mapping)




# step 2: import files

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# df = pd.read_json('/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/tweet_sentiment.json', lines=True)
# df.to_json('mlb_map.json',orient='table')


def do_geocode(location):
    geolocator = Nominatim(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
    try:
        return geolocator.geocode(location ,timeout=None)
        time.sleep(1)
    except GeocoderTimedOut:
        return do_geocode(location)
    except geopy.exc.GeocoderUnavailable:
        return do_geocode(location)


# step 3: send to es
with open('mlb_map.json', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        data_list = json.loads(line)['data']
        try:
            for data in data_list:
                location = data["user"]["location"]
                location_more = do_geocode(location)
                if location_more:
                    location_latitude = location_more.latitude
                    location_longitude = location_more.longitude
                    print((location_latitude, location_longitude))
                    es.index(index="mlb_map_02",
                             body={
                                   "author": data["user"]["name"],
                                   "author_screen_name": data["user"]["screen_name"],
                                   "location": {'lat':location_latitude,'lon':location_longitude},
                                   "location_keyword" : data["user"]["location"],
                                   "device" : data['source'].split('>')[-2].split('</a')[0],
                                   "date": data["created_at"].replace('+0000 ', ''),
                                   "message": data["text"],
                                   "followers_count": data["user"]["followers_count"],
                                   "friends_count": data["user"]["friends_count"],
                                   "favourites_count": data["user"]["favourites_count"],
                                   "hashtags": data['entities']['hashtags'],
                                   "lang": data["lang"],
                                   "timestamp_ms": data["timestamp_ms"]
                             },
                             request_timeout=100000)
                    print(".......................keeping sending")
        except IndexError:
            continue



print('finnished')



# location = geolocator.geocode("175 5th Avenue NYC")
# location = geolocator.reverse("44.9504037, -93.1015026")
# print(location.address)
# print((location.latitude, location.longitude))
# print(location.raw)