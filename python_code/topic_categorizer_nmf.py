from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

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

stop_words = set(stopwords.words('english'))
word_rooter = nltk.stem.snowball.PorterStemmer(ignore_stopwords=False).stem

# pd.set_option("display.max_rows", None, "display.max_columns", None)

# import and clean all tweets
def clean_text():
# import the json file and extract the text entries
	tweet = []
	all_tweets = []
	with open('trumptweets.json', 'r') as f:
		trump_dict = json.load(f)
		trump_tweet_list = []
		for tweet in trump_dict:
			data = tweet["text"], tweet["created_at"]
			trump_tweet_list.append(data)
# clean the text
		for tweet in trump_tweet_list:
			text = tweet[0]
			#remove hyperlinks
			text = re.sub(r'https.*', '', text)
			text = text.replace('&amp', '')
			text = text.replace('U.S.', 'usa')
			text = text.replace('dems', 'democrats')
			text = text.replace('RT', '')
			# lemmatizer = WordNetLemmatizer()
			# text = ' '.join([lemmatizer.lemmatize(w) for w in text])
		# split tweets into tokens by white space
			tokens = text.split()
			# make lower case
			tokens = [word.lower() for word in tokens]
		# Remove punctuation no roman alphabet words from each tweet, except for # and @
		# preserve numbers( use is aplha for just letters, is alnum for letters and numbers)
			tokens = ["".join(c for c in word if c.isalnum()) for word in tokens]
			tokens = [w for w in tokens if not w in stop_words]
			tweet = ' '.join(tokens)
			all_tweets.append(tweet)
		tweet_data = pd.DataFrame(all_tweets, columns = ["tweet_data"])
		return tweet_data

data = clean_text()
# print(data)
# may need to stem the data
# the vectorizer object will be used to transform text to vector form
vectorizer = CountVectorizer(max_df = 0.1, min_df=3)
# apply transformation
tf = vectorizer.fit_transform(data["tweet_data"])
# tf_feature_names tells us what word each column in the matric represents
tf_feature_names = vectorizer.get_feature_names()
from sklearn.decomposition import LatentDirichletAllocation
number_of_topics = 10
model = LatentDirichletAllocation(n_components=number_of_topics, random_state=0)
model.fit(tf)
def display_topics(model, feature_names, no_top_words):
	topic_dict = {}
	for topic_idx, topic in enumerate(model.components_):
		topic_dict["Topic %d words" % (topic_idx)] = ['{}'.format(feature_names[i])
													  for i in topic.argsort()[:-no_top_words - 1:-1]]
		topic_dict["Topic %d weights" % (topic_idx)] = ['{:.1f}'.format(topic[i])
														for i in topic.argsort()[:-no_top_words - 1:-1]]
	return pd.DataFrame(topic_dict)

# display LDA results
# no_top_words = 10
# topics = display_topics(model, tf_feature_names, no_top_words)
# pd.set_option("display.max_rows", None, "display.max_columns", None)
# print("LDA results:\n")
# print(topics)


# # Do a NMF model
# i is the number of topics, no_top_words = number of words in the topic list
for i in range(9,15,2):
	no_top_words = 8
	model = NMF(n_components=i, random_state=0, max_iter=500, alpha=.1, l1_ratio=.5)
	model.fit(tf)
	nmf_topics = display_topics(model, tf_feature_names, no_top_words)
	pd.set_option("display.max_rows", None, "display.max_columns", None)
	print(f"NMF results: for {i} topics.")
	print(nmf_topics)


 
# # how does kmeans work
# model = KMeans (n_clusters = 10)
# model.fit(tf)
# clusters=model.labels_.tolist()

# if opts.n_components:
#     original_space_centroids = svd.inverse_transform(km.cluster_centers_)
#     order_centroids = original_space_centroids.argsort()[:, ::-1]
# else:
#     order_centroids = km.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# for i in range(true_k):
#     print("Cluster %d:" % i, end='')
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind], end='')
#     print()





# #kmeans clustering optimal group size, the elbow method, optimal is wher the curve starts to flatten out

# # kmeans_topics = display_topics(model, tf_feature_names, no_top_words)
# # pd.set_option("display.max_rows", None, "display.max_columns", None)
# # print("KMEANS results:\n ")
# # print(kmeans_topics)

# #try to add BERT to LDA model
