# https://medium.com/better-programming/twitter-sentiment-analysis-15d8892c0082

import pandas as pd
import json
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# read data
df = pd.read_csv('/Users/kao_oak/PycharmProjects/Twitter/Moduel_Ball/NLTK/search-mlb.csv')


# Create a function to clean the tweets

def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
    text = re.sub('#', '', text)  # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text)  # Removing RT
    text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink

    return text


# Clean the tweets
df['tweet'] = df['tweet'].apply(cleanTxt)

# Show the cleaned tweets
# print(df)


# Create a function to get the subjectivity

def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity

def getPolarity(text):
   return  TextBlob(text).sentiment.polarity

# Create two new columns 'Subjectivity' & 'Polarity'

df['Subjectivity'] = df['tweet'].apply(getSubjectivity)
df['Polarity'] = df['tweet'].apply(getPolarity)

# Show the new dataframe with columns 'Subjectivity' & 'Polarity'
# print(df)

# Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

# store data to csv
df.to_csv('search-mlb_v2', index = False)

# Show the dataframe
# print(df)

# word cloud visualization
# allWords = ' '.join([twts for twts in df['tweet']])
# wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)
#
# plt.imshow(wordCloud, interpolation="bilinear")
# plt.axis('off')
# plt.show()

# Printing positive tweets
# print('Printing positive tweets:\n')
# j=1
# sortedDF = df.sort_values(by=['Polarity']) #Sort the tweets
# for i in range(0, sortedDF.shape[0] ):
#   if( sortedDF['Analysis'][i] == 'Positive'):
#     print(str(j) + ') '+ sortedDF['tweet'][i])
#     print()
#     j= j+1

#
# # Printing negative tweets
# print('Printing negative tweets:\n')
# j=1
# sortedDF = df.sort_values(by=['Polarity'],ascending=False) #Sort the tweets
# for i in range(0, sortedDF.shape[0] ):
#   if( sortedDF['Analysis'][i] == 'Negative'):
#     print(str(j) + ') '+sortedDF['tweet'][i])
#     print()
#     j=j+1


# Plotting
# plt.figure(figsize=(8,6))
# plt.scatter(df["Polarity"], df["Subjectivity"], color='Blue')
#
# # for i in range(0, df.shape[0]):
# #   plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue')
#
# # plt.scatter(x,y,color)
# plt.title('Sentiment Analysis')
# plt.xlabel('Polarity')
# plt.ylabel('Subjectivity')
# plt.show()


