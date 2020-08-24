import plotly.express as px
import seaborn as sns
import re
import csv
import string
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

# get search term
# make a searchable datbase with options for whicj values to search

def get_input():
    search_term = input("Please enter a search term to get all tweets containing that word:\n")
    search_term = search_term.lower()
    return (search_term)
# import and clean all tweets
def import_data():
# import the csv file and extract the text entries
    search_term = get_input()
    with open('condensed_dow_and_sentiment.csv', 'r') as f:
        csvReader = csv.DictReader(f)
        dow_tweet_list = []
        clean_tweet_list = []
        for row in csvReader:
            data = row["Time"], row["Vader_compound"],row["Volatility"], row["Open"],row["Close"],row["Tweet_text"], row["Volume"]
            dow_tweet_list.append(data)
        print(dow_tweet_list)
        for tweet in dow_tweet_list:
            time = tweet[0]
            sentiment = tweet[1]
            dow_volatility = tweet[2]
            dow_open = tweet[3]
            dow_close = tweet[4]
            text = tweet[5]
            dow_volume = tweet[6]
            text = re.sub(r'https.*', ' ', text)
            lower_text = text.lower()
            content_word_tweets = time, sentiment, dow_volatility, dow_open, dow_close, text, dow_volume	
        #searching for user input term (lower case)
            if search_term in lower_text:
                clean_tweet_list.append(content_word_tweets)
        user_text = clean_tweet_list
        # calculate the number of tokens and start sentiment analysis
        if (len(user_text))>0:
            print(f"The 2016-2020 database holds {len(user_text)} tweets with the search term {search_term}")
            df = pd.DataFrame(user_text, columns = ["Time", "Vader_compound", "Volatility", "Open","Close", "Text", "Volume"])
            return df, search_term             
        # if search term doesn't appear restart the input process
        else:
            print(f"{user_text} does not appear in the database")
            import_data()


    # create a dataframe of our results
    # df = pd.DataFrame(dow_tweet_list, columns = ["Time", "Vader_compound", "High", "Low", "Text"]) 
    # print(df)

    # # convert "created at" to datetime
    # df["Time"] = pd.to_datetime(df["Time"],
    # infer_datetime_format = "%d/%m/%Y", utc = True)


# def graph_function(user_text, search_term):
#     print(search_term)


df, search_term = import_data()
print(search_term)
x_axis = input("You can plot the data for 'Time', Dow Jones 'High' or 'Low' and 'Vader_compound \n"
               "Please choose 'Time', 'Volatility', 'Open', 'Close', 'Volume' or 'Vader_compound\n"
               "Please enter a value for the x axis:\n")
y_axis = input("Please enter a value for the y axis: \n")

if x_axis and y_axis in["Time", "Volatility", "Open","Close", "Volume", "Vader_compound"]:

# figure comparing two input variables from user
    fig = px.scatter(df, x=x_axis, y= y_axis, hover_data = ["Time", "Text"])
#https://plotly.com/python/hover-text-and-formatting/#customizing-hover-text-with-plotly-express
    fig.update_layout(
        title={
            'text': "Results for: " + search_term,
            'y': 0.99,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.show()
else:
    print("Please input 'Time', 'Volatility', 'Open, 'Close', 'Volume' or 'Vader_compound'")
