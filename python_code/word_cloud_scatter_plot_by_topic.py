import plotly.express as px
import seaborn as sns
import re
import csv
import string
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


pd.set_option("display.max_rows", None, "display.max_columns", None)

# get search term
# make a searchable datbase with options for whicj values to search


def word_cloud(user_text):
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


# import and clean all tweets
def import_data():
# import the csv file and extract the text entries
	search_term_list = ['border', 'strong', 'military', 'endorsement', 'total', 'crime', 'vote', 'vets']
	with open('condensed_dow_and_sentiment.csv', 'r') as f:
		csvReader = csv.DictReader(f)
		tweet_list = []
		original_tweet_list = []
		clean_tweet_list = []
		for row in csvReader:
			data = row["Time"], row["Vader_compound"],row["Volatility"], row["Open"],row["Close"],row["Tweet_text"], row["Volume"]
			tweet_list.append(data)
		for tweet in tweet_list:
			time = tweet[0]
			sentiment = tweet[1]
			dow_volatility = tweet[2]
			dow_open = tweet[3]
			dow_close = tweet[4]
			text = tweet[5]
			dow_volume = tweet[6]
			if len(text)>5:
				text = re.sub(r'https.*', ' ', text)
				text = text.replace('&amp', '')
				text = text.replace('U.S.', 'usa')
				text = text.replace('dems', 'democrats')
				text = text.replace('RT', '')
				text = text.replace('-', '')
				text = text.replace('?', '')
				text = text.replace('.', '')
				text = text.replace('#', '')
				text = text.replace('@', '')
				text = text.lower()
				tokens = text.split()
				tokens = [w for w in tokens if not w in stop_words]
				print(tokens)
				listToStr = ' '.join(map(str, tokens))
				content_word_tweets = time, sentiment, dow_volatility, dow_open, dow_close, listToStr, dow_volume	
			#searching for user input term (lower case)
				for word in search_term_list:
					if word in tokens:
						clean_tweet_list.append(content_word_tweets)
						original_tweet_list.append(tweet)
				user_text = clean_tweet_list
		df = pd.DataFrame(clean_tweet_list, columns = ["Time", "Sentiment","A", "B", "C", "Text", "F"]) 
		df["Tweet"] = original_tweet_list
		df = df.drop(columns = ["A", "B", "C", "F"])
		word_cloud(user_text)
		return df, search_term_list

df, search_term_list = import_data()
search_terms = ' '.join(map(str, search_term_list))

fig = px.scatter(df, x="Time", y= "Sentiment", hover_data=["Tweet", "Sentiment"])
fig.update_layout(
		title={
			'text': "Results for: " + search_terms,
			'y': 0.99,
			'x': 0.5,
			'xanchor': 'center',
			'yanchor': 'top'})
fig.show()


