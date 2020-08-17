import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import re
import json
import string
import matplotlib.pyplot as plt
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
pd.set_option("display.max_rows", None, "display.max_columns", None)

# get search term and conver to lower case
def get_input(): 
    search_term = input("Please enter a search term:\n")
    search_term = search_term.lower()
    return (search_term)

def clean_text():
    search_term = get_input()
# import the json file and extract the text entries
    with open('json/trumptweets.json', 'r') as f:
        trump_dict = json.load(f)
        trump_tweet_list = []
        for tweet in trump_dict:
            data = tweet["text"], tweet["created_at"]
            trump_tweet_list.append(data)
# clean the text
        clean_tweet_list = []
        #remove hyperlinks
        for tweet in trump_tweet_list:
            text = tweet[0]
            time = tweet[1]
            text = re.sub(r'https.*', ' ', text)
            lower_text = text.lower()
            content_word_tweets = text,time	
	# searching for user input term (lower case)
            if search_term in lower_text:
                clean_tweet_list.append(content_word_tweets)
        user_text = clean_tweet_list
	# calculate the number of tokens and start sentiment analysis
        if (len(user_text))>0:
            print(f"In 2018 there were {len(user_text)} tweets with the search term {search_term}")
            sentiment_analyzer(user_text, search_term)
        #if search term doesn't appear restart the input process
        else:
            print(f"{user_text} does not appear in the database")
            clean_text()

# # do Vader Analysis
def sentiment_analyzer(user_text, search_term):
    i = 0
    vader_sentiment = []
    vader_pos = []
    vader_neg = []
    vader_neutral = []
    vader_compound = []
    time_stamp = []
    while i < len(user_text):
        data = user_text[i]
        text=data[0]
        time=data[1]
        # vader analyzer returns a category (negative, neutral, positive)
        # and returns a ranking for each category (adding up to 1)
        #we take the compound value
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
    # convert "created at" to datetime
    df["Time"] = pd.to_datetime(df["Time"],
    infer_datetime_format = "%d/%m/%Y", utc = False)
    print(df)
    # plot the  sentiment analysis
    fig = px.line(df, x='Time', y="Vader_compound")
    fig.update_layout(
        title={
            'text': "Sentiment Over Time",
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.show()
    df.to_csv('sentiment.csv')
    # word_cloud(user_text,search_term)

# create word clouds
# convert all the tweets into a single list
def word_cloud(user_text, search_term):
    #function to flatten the data array
    def flatten(user_text): return [
        item for sublist in user_text for item in sublist]
    word_cloud_text = flatten(user_text)
    # create a word cloud object
    wc = WordCloud(width=800, height=800,
                background_color='white',
                min_font_size=10)
    #call word cloud
    img = wc.generate_from_text(' '.join(word_cloud_text))
    #plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(img)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

clean_text()
