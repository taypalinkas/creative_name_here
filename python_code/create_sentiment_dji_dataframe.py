import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import re
import json
import csv
import string
import matplotlib.pyplot as plt
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
# pd.set_option("display.max_rows", None, "display.max_columns", None)

# import and clean all tweets
def clean_text():
# import the json file and extract the text entries
    all_tweets = []
    with open('../json/trumptweets.json', 'r') as f:
        trump_dict = json.load(f)
        trump_tweet_list = []
        for tweet in trump_dict:
            data = tweet["text"], tweet["created_at"]
            trump_tweet_list.append(data)
# clean the text
        #remove hyperlinks
        for tweet in trump_tweet_list:
            text = tweet[0]
            time = tweet[1]
            text = re.sub(r'https.*', ' ', text)
            tweets = text,time
            all_tweets.append(tweets)
        sentiment_analyzer(all_tweets)

# # do Vader Analysis
def sentiment_analyzer(all_tweets):
    i = 0
    tweet_text = []
    vader_sentiment = []
    vader_pos = []
    vader_neg = []
    vader_neutral = []
    vader_compound = []
    time_stamp = []
    while i < len(all_tweets):
        data = all_tweets[i]
        text=data[0]
        time=data[1]
        # vader analyzer returns a category (negative, neutral, positive)
        # and returns a ranking for each category (adding up to 1)
        #we take the compound value
        tweet_text.append(text)
        vader_test = analyser.polarity_scores(text)
        vader_sentiment.append(vader_test)
        vader_compound.append(vader_sentiment[i]["compound"])
        vader_pos.append(vader_sentiment[i]["pos"])
        vader_neg.append(vader_sentiment[i]["neg"])
        vader_neutral.append(vader_sentiment[i]["neu"])
        time_stamp.append(time)
        i += 1
    # create a datfarem of our results
    df = pd.DataFrame(vader_compound, columns = ["Vader_compound"]) 
    # print(user_text)
    df["Vader_pos"] = vader_pos
    df["Vader_neg"]= vader_neg
    df["Vader_neutral"] = vader_neutral
    df["Time"] = time_stamp 
    df["Tweet_text"] = tweet_text
    # convert "created at" to datetime
    df["Time"] = pd.to_datetime(df["Time"],
    infer_datetime_format = "%d/%m/%Y", utc = True)
    
    #import dow data and create dataframe
    dow_data = dow_jones()
    dow_df = pd.DataFrame(dow_data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    #convert dow data to datetime
    dow_df["Date"] = pd.to_datetime(dow_df["Date"],
    infer_datetime_format="%Y/%m/%d", utc=True)
    # sort dataframes  by date
    df = df.sort_values('Time')
    dow_df = dow_df.sort_values('Date')
   # merge tweet dataframe and dow dataframe 
    final_df = pd.merge_asof(df,dow_df, left_on="Time", right_on="Date")
    # final_df.drop(columns="Time")
    cols_to_order = ['Time', 'Vader_compound', "High", "Low"]
    new_columns = cols_to_order + (final_df.columns.drop(cols_to_order).tolist())
    final_df = final_df[new_columns]
    final_df.to_csv('dow_and_sentiment.csv')
    condensed_df = final_df.drop(columns=["Date","Vader_pos", "Vader_neg", "Vader_neutral", "Open","Close", "Volume"])
    condensed_df.to_csv('condensed_dow_and_sentiment.csv')

def dow_jones():
# import the Dow Jones CSV, minus adjusted close
    with open('DJI.csv', 'r') as f:
        csvReader = csv.DictReader(f)
        dow_data = []
        for row in csvReader:
            data = row["Date"], row["Open"], row["High"], row["Low"], row["Close"], row["Volume"]
            dow_data.append(data)
    return dow_data
clean_text()
