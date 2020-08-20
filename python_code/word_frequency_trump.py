# useful functions for NLP: Load Document, Clean document
# cut a doc into fixed sized sequences of tokens, save doc
# load doc into memory
import nltk
from nltk.stem import WordNetLemmatizer
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()
import pandas as pd
import matplotlib.pyplot as plt
import string
import json
import csv
import numpy as np
import re
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud, STOPWORDS

# remove '#' from puctuation to remove to preserve hashtags
# punct_to_remove = string.punctuation
# punct_to_remove = punct_to_remove.replace("#", "")
# punct_to_remove = punct_to_remove.replace("@", "")

pd.set_option("display.max_rows", None, "display.max_columns", None)
#import standard stopwords from NLTK, may need to customize this list
stop_words = set(stopwords.words('english'))

# take the original tweets , remove stopwords and punctuation other than #,#, 
# remove some unneccessary tokens and make everything lowercasse: create a datfram with sentiemht and TimeoutError

def clean_punct(text):
	punctuations = """!()-[]''{}"";:,<>./?$%^&*_~"""
	no_punct = ""
	for char in text:
		if char not in punctuations:
			no_punct = no_punct + char
	return no_punct

def clean_data():
	clean_tweet_list = []
	total_tokens = 0  # import the csv file and extract the text entries
	with open('condensed_dow_and_sentiment.csv', 'r') as f:
		csvReader = csv.DictReader(f)
		tweet_list = []
		clean_tweet_list = []
		time_list = []
		Vader_list = []
	
		for row in csvReader:
			data = row["Tweet_text"], row["Time"], row["Vader_compound"]
			tweet_list.append(data)
# clean the text
	for tweet in tweet_list:
		text = tweet[0]
		# text = clean_punct(text)
		time = tweet[1]
		Vader_compound = tweet[2]
		#remove RT, &amp, hyperlinks: preserve U.S.
		# tweet[0] = tweet[0].str.replace("[^a-zA-Z#]", " ")

		text = re.sub(r'https.*', '', text)
		text = text.replace('&amp', '')
		text = text.replace('U.S.', 'usa')
		text = text.replace('RT', '')
		text = text.replace(';', '')
		text = text.replace('-', '')

		# split tweets into tokens by white space
		tokens = text.split()
		# make lower case
		tokens = [word.lower() for word in tokens]

#	Remove punctuation from each tweet, except for
		# table = str.maketrans('', '', string.punctuation)
		# tokens = [w.translate(table) for w in tokens]
	# Remove tokens that are not alphabetic?
		# tokens = [word for word in tokens if word.isalpha()]
	# should we lematize tokens: maybe not
		# lemmatizer = WordNetLemmatizer()
		# lemmas = ' '.join([lemmatizer.lemmatize(w) for w in tokens])

	# remove stop words
		content_word_tweet = [w for w in tokens if not w in stop_words]
		number_of_tokens = len(content_word_tweet)
	# calculate the number of tokens
		clean_tweet_list.append(content_word_tweet)	
		time_list.append(time)
		Vader_list.append(Vader_compound)	

		total_tokens = total_tokens+number_of_tokens
	# print(f"tweets with search term {clean_tweet_list}")
	# print(f"In the data set there are {len(clean_tweet_list)} tweets")
	# print(f"In the data set there are  {total_tokens} tokens/words")
	word_frequency_df = pd.DataFrame(clean_tweet_list)
	word_frequency_df["Time"] = time_list
	word_frequency_df["Vader_compound"] = Vader_list
	# print (word_frequency_df) 
	print(len(clean_tweet_list), len(time_list),len(Vader_list))
	return clean_tweet_list, word_frequency_df

# def to count word frquency and make a vocab list of all words used
def word_counter():
	hashtags = []
	references = []
	data = clean_data()
	# results is the cleaned tweets
	results = data[0]
	#dataframe includes vader score and time
	results_df = data[1]
	# print(results_df)
	# Create a dataframe with the vocabulary and their tweet ids
	DF = {}
	for i in range(len(results)):
		tokens = results[i]
		for w in tokens:
			try:
				DF[w].add(i)
			except:
				DF[w] = {i}

	for word in DF:
		#get the number of occurences of each word
		DF[word] = len(DF[word])
		#extract the words with # and @
		if '#' in word:
			hashtags.append(word)
		if '@' in word:
			references.append(word)
	from collections import Counter
	# print(references)
	# number = Counter(references)
	print(f"sample references: {references[0:9]} sample hashtags {hashtags[0:9]}")
	print(f"There are {len(hashtags)} hashtags \n there are {len(references)} references")

	# DF.keys is the lst of words
	# DF.values is the tweet ID
	# print(DF.items())
	
	#Create a list of words sorted by their frequency
	sorted_frequency = sorted(DF.items(), key = lambda x: x[1], reverse = True)
	print(f"The top 20 words are {sorted_frequency[0:19]}")
	# create a list of unique words
	total_vocab = [x for x in DF]
	print(f"There are {len(total_vocab)}  words after removing stop words, but the list needs cleaning")

word_counter()

# Things to work on
# combine u.s., u.s.a., america? 
# remove stop words first?
# do lemmatization?
# some names are connected together
# some hashtags, foreign words and emoticons. The n-grams are hashtags
#2268 are retweets
# remove "&amp"

# remove twitter handles
# def remove_pattern(input_txt, pattern):
#   r = re.findall(pattern, input_txt)
#   for i in r:
#     input_txt = re.sub(i, '', input_txt)

#   return input_txt

# combi['tidy_tweet'] = np.vectorize(remove_pattern)(combi['tweet'], "@[\w]*")
# Remove special characters, numbers, punctuation

# combi['tidy_tweet'] = combi['tidy_tweet'].str.replace("[^a-zA-Z#]", " ")
