# https://towardsdatascience.com/twitter-sentiment-analysis-using-fasttext-9ccd04465597
import concurrent.futures
import time
import pandas as pd
from textblob import TextBlob
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import json
import emot
from emot.emo_unicode import UNICODE_EMO, EMOTICONS

# self defined contractions
def load_dict_contractions():
    return {
        "ain't": "is not",
        "amn't": "am not",
        "aren't": "are not",
        "can't": "cannot",
        "'cause": "because",
        "couldn't": "could not",
        "couldn't've": "could not have",
        "could've": "could have",
        "daren't": "dare not",
        "daresn't": "dare not",
        "dasn't": "dare not",
        "didn't": "did not",
        "doesn't": "does not",
        "don't": "do not",
        "e'er": "ever",
        "em": "them",
        "everyone's": "everyone is",
        "finna": "fixing to",
        "gimme": "give me",
        "gonna": "going to",
        "gon't": "go not",
        "gotta": "got to",
        "hadn't": "had not",
        "hasn't": "has not",
        "haven't": "have not",
        "he'd": "he would",
        "he'll": "he will",
        "he's": "he is",
        "he've": "he have",
        "how'd": "how would",
        "how'll": "how will",
        "how're": "how are",
        "how's": "how is",
        "i'd": "I would",
        "i'll": "I will",
        "i'm": "I am",
        "i'm'a": "I am about to",
        "i'm'o": "I am going to",
        "isn't": "is not",
        "it'd": "it would",
        "it'll": "it will",
        "it's": "it is",
        "i've": "I have",
        "kinda": "kind of",
        "let's": "let us",
        "mayn't": "may not",
        "may've": "may have",
        "mightn't": "might not",
        "might've": "might have",
        "mustn't": "must not",
        "mustn't've": "must not have",
        "must've": "must have",
        "needn't": "need not",
        "ne'er": "never",
        "o'": "of",
        "o'er": "over",
        "ol'": "old",
        "oughtn't": "ought not",
        "shalln't": "shall not",
        "shan't": "shall not",
        "she'd": "she would",
        "she'll": "she will",
        "she's": "she is",
        "shouldn't": "should not",
        "shouldn't've": "should not have",
        "should've": "should have",
        "somebody's": "somebody is",
        "someone's": "someone is",
        "something's": "something is",
        "that'd": "that would",
        "that'll": "that will",
        "that're": "that are",
        "that's": "that is",
        "there'd": "there would",
        "there'll": "there will",
        "there're": "there are",
        "there's": "there is",
        "these're": "these are",
        "they'd": "they would",
        "they'll": "they will",
        "they're": "they are",
        "they've": "they have",
        "this's": "this is",
        "those're": "those are",
        "'tis": "it is",
        "'twas": "it was",
        "wanna": "want to",
        "wasn't": "was not",
        "we'd": "we would",
        "we'd've": "we would have",
        "we'll": "we will",
        "we're": "we are",
        "weren't": "were not",
        "we've": "we have",
        "what'd": "what did",
        "what'll": "what will",
        "what're": "what are",
        "what's": "what is",
        "what've": "what have",
        "when's": "when is",
        "where'd": "where did",
        "where're": "where are",
        "where's": "where is",
        "where've": "where have",
        "which's": "which is",
        "who'd": "who would",
        "who'd've": "who would have",
        "who'll": "who will",
        "who're": "who are",
        "who's": "who is",
        "who've": "who have",
        "why'd": "why did",
        "why're": "why are",
        "why's": "why is",
        "won't": "will not",
        "wouldn't": "would not",
        "would've": "would have",
        "y'all": "you all",
        "you'd": "you would",
        "you'll": "you will",
        "you're": "you are",
        "you've": "you have",
        "Whatcha": "What are you",
        "luv": "love",
        "sux": "sucks"
    }

def read_csv(filename):
    df = pd.read_csv(filename,delimiter="\t",header=None)
    return df

def read_json(filename):
    pd.set_option('display.max_colwidth',10000)
    df = pd.read_json(filename, lines=True)
    return df


# Function for converting emojis into word
def convert_emojis(tweet):
    for emot in UNICODE_EMO:
        tweet = tweet.replace(emot, "_".join(UNICODE_EMO[emot].replace(","," ").replace(":"," ").split()))
    return tweet

# Function for converting emoticons into word
def convert_emoticons(tweet):
    for emot in EMOTICONS:
        tweet = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(","," ").split()), tweet)
    return tweet

def cleanTxt(tweet):
    tweet=str(tweet)
    tweet = re.sub('@[A-Za-z0–9]+', '', tweet)  # Removing @mentions
    tweet = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", tweet)  # Removing '#' hastags/account
    # tweet = re.sub('RT[\s]+', '', tweet)  # Removing RT
    tweet= re.sub('https?:\/\/\S+', '', tweet)  # Removing hyperlink
    tweet= re.sub('pic\.twitter\.com\/[A-Za-z0–9]', '', tweet)  # Removing com
    tweet = re.sub("[\.\,\!\?\:\;\-\=]", " ", tweet)  # Remove punctuations
    tweet = tweet.replace('\x92', "'")  # Special case not handled previously.
    # tweet = re.sub('\d', '', tweet)  # Removing number
    tweet = tweet.lower()


    CONTRACTIONS = load_dict_contractions()
    tweet = tweet.replace("’", "'")
    words = tweet.split()
    reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
    tweet = " ".join(reformed)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

    # tweet = word_tokenize(tweet)

    return tweet

def getSubjectivity(tweet):
    tweet = str(tweet)
    return TextBlob(tweet).sentiment.subjectivity

# Create a function to get the polarity

def getPolarity(tweet):
    tweet = str(tweet)
    return  TextBlob(tweet).sentiment.polarity

def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'

import os
dir_locate = "/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/re-search/" #資料夾目錄
files = os.listdir(dir_locate) # 得到資料夾下的所有檔名稱

for path in files:
    name = path.split('.')[0]
    # print(name)
    path_url = "/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/re-search/"+path

    try:
        # read data

        df= read_json(path_url)
        stop_words = stopwords.words('english')
        my_stopword_list = ['world', 'pic', 'twitter', 'new', 'games', 'game', 'home', 'history', 'babe', 'time', 'letter',
                            'played','live','see', 'month', 'told', 'says','man',
                            'pre', 'custom', 'hey', 'past', 'someone', 'side', 'include', 'may', 'clean', 'year', 'old',
                            'day', 'long', 'one', 'guy', 'even','always','would','us','daily','two','get','today','every'
                                                         'go']
        df = df.iloc[:, 0:31]
        # print(df.info())

        df['clean_tweet'] = df['tweet'].apply(cleanTxt).apply(convert_emojis).apply(convert_emoticons)\
            # .apply(
            # lambda x: [item for item in x if item not in stop_words]).apply(
            # lambda x: [item for item in x if item not in my_stopword_list])
        # print(df['clean_tweet'])
        df['Subjectivity'] = df['clean_tweet'].apply(getSubjectivity)
        df['Polarity'] = df['clean_tweet'].apply(getPolarity)
        df['Analysis'] = df['Polarity'].apply(getAnalysis)

        df.to_json(name+'_v1.json',orient='table')
        print('..........')
    except UnicodeDecodeError:
        continue

    print(name+'...............finished')

print('all finished')



#
# start = time.time()
# finish = time.time()
# print(f'Finished'+name+' in {round(finish - start, 2)} seconds')
# # 多線程的方式
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     try:
# #         results = executor.map(main, path_url_list)
#
#
#     # 為了把結果印出來
#     for result in results:
#         print(result)




