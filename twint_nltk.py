import twint

# Setup Twint for scrapping tweets
search = ('Boston Red Sox,MLB,New York Yankees,Chicago White Sox,Cleveland Indians,Detroit Tigers,Baltimore Orioles,Oakland Athletics,Minnesota Twins,Atlanta Braves,Miami Marlins,New York Mets,Philadelphia Phillies,Washington Nationals,Chicago Cubs,Cincinnati Reds,Milwaukee Brewers,Pittsburgh Pirates,St. Louis Cardinals,Arizona Diamondbacks,Colorado Rockies,Los Angeles Dodgers,San Diego Padres,San Francisco Giants')

search_list = search.split(',')


for i in search_list:
    # print(i)
    # print(type(i))
    i = i.lower()
    c = twint.Config()
    c.Search = i
    # c.Elasticsearch = "http://34.80.0.41:9200/"
    c.Min_likes = 10
    c.Lowercase = True
    i = i.replace(' ','')
    c.Index_tweets = 'search-{}'.format(i)
    c.Store_json = True
    c.Output = 'search-{}.json'.format(i)
    c.Since = "2016-01-01 00:00:00"
    c.Count = True
    c.Pandas = True
    # c.Custom = " username | tweets"

    # c.Store_object_follow_list
    # c.Store_object_tweets_list
    # c.Store_object_users_list

    # # Run
    try:
        twint.run.Search(c)
    except Exception as e:
        print(e)


print('finished')