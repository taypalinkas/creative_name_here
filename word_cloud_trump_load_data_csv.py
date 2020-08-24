from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import plotly.express as px
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import re
import json
import csv
import string
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
pd.set_option("display.max_rows", None, "display.max_columns", None)

#import standard stopwords from NLTK, may need to customize this list
stop_words = set(stopwords.words('english'))
# import the csv file and extract the text entries
def clean_data():
	with open('python_code/condensed_dow_and_sentiment.csv', 'r') as f:
		csvReader = csv.DictReader(f)
		trump_tweet_list = []
		for tweet in csvReader:
			data = tweet["Time"], tweet["Vader_compound"], tweet["Tweet_text"]
			trump_tweet_list.append(data)
	# clean the text
		clean_tweet_list = []
		all_times = []
		all_sentiments = []
		#remove hyperlinks
		for tweet in trump_tweet_list:
			text=(tweet[2])
			time= (tweet[0])
			sentiment = (tweet[1])
			# time = tweet[0]
			# sentiment = tweet[1]
			# text = tweet[2]
			text = re.sub(r'https.*', '', text)
			text = text.replace('&amp', '')
			text = text.replace('U.S.', 'usa')
			text = text.replace('RT', '')
			lemmatizer = WordNetLemmatizer()
			text = lemmatizer.lemmatize(text)
			# split tweets into tokens by white space
			tokens = text.split()
			# make lower case
			tokens = [word.lower() for word in tokens]
			tokens = ["".join(c for c in word if c.isalnum() or c ==
							"#" or c == "@") for word in tokens]
			tokens = [w for w in tokens if not w in stop_words]
			tweet = ' '.join(tokens)
			clean_tweet_list.append(tweet)
			all_times.append(time)
			all_sentiments.append(sentiment)
		tweet_data = pd.DataFrame(clean_tweet_list, columns=["Tweet_data"])
		tweet_data["Time"] = all_times
		tweet_data["sentiment"] = all_sentiments
		return(tweet_data)

def categorizor():
	data = clean_data()
	# print(data)
	# may need to stem the data
	# the vectorizer object will be used to transform text to vector form
	vectorizer = CountVectorizer(max_df=0.1, min_df=3)
	# apply transformation
	tf = vectorizer.fit_transform(data["Tweet_data"])
	# tf_feature_names tells us what word each column in the matric represents
	tf_feature_names = vectorizer.get_feature_names()
	number_of_topics = 10
	model = LatentDirichletAllocation(
		n_components=number_of_topics, random_state=0)
	model.fit(tf)

	def display_topics(model, feature_names, no_top_words):
		topic_dict = {}
		for topic_idx, topic in enumerate(model.components_):
			topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(feature_names[i])
												for i in topic.argsort()[:-no_top_words - 1:-1]]
			topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(topic[i])
												  for i in topic.argsort()[:-no_top_words - 1:-1]]
		return pd.DataFrame(topic_dict)

	# # Do a NMF model
	# i is the number of topics, no_top_words = number of words in the topic list
	for i in range(9, 10, 3):
		no_top_words = 10
		model = NMF(n_components=i, random_state=0, alpha=.1, l1_ratio=.5)
		model.fit(tf)
		nmf_topics = display_topics(model, tf_feature_names, no_top_words)
		pd.set_option("display.max_rows", None, "display.max_columns", None)
		print(f"NMF results: for {i} topics.")
		return nmf_topics, data

def plot_data ():
	figure_data = []
	plot_data = categorizor()
	topics = plot_data[0]
	dataset= plot_data[1]
	print(type(dataset), type(topics))
	search_terms = topics["Topic 4 words"].values.tolist()
	tweet_text = dataset["Tweet_data"].values.tolist
	print(type(tweet_text))
	# for tweet in tweet_text:
	# 	for i in range(len(search_terms)):
	# 		if search_terms[i] in tweet:
	# 			figure_data.append(tweet)
	# print(figure_data)

# 	time = dataset["Time"]
# 	sentiment = dataset["sentiment"]
	# print(search_terms)
	# print(type(search_terms))
	# for tweet in tweet_text:
	# 	for word in tweet:
	# 		if word in search_terms:
	# 			figure_data.append(tweet)	
	# print(figure_data)
	
	
	
	# plot_df = dataset.loc[dataset['Tweet_data'].isin(search_terms)]
	# fig = px.scatter(plot_df, x="Time", y= "sentiment", hover_data = "tweet_text")
	# fig.update_layout(
	# 			title={
	# 				'text': "Results for: ",
	# 				'y': 0.99,
	# 				'x': 0.5,
	# 				'xanchor': 'center',
	# 				'yanchor': 'top'})
	# fig.show()
plot_data()
