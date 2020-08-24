
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
#import standard stopwords from NLTK, may need to customize this list
stop_words = set(stopwords.words('english'))

# take the original tweets , remove stopwords and punctuation other than #,#, 
# remove some unneccessary tokens and make everything lowercase: create a datframe with sentiment and Time


from nltk.corpus import wordnet

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def clean_data():
	clean_tweet_list = []
	total_tokens = 0  
	# import the csv file and extract the text entries
	with open('condensed_dow_and_sentiment.csv', 'r') as f:
		csvReader = csv.DictReader(f)
		tweet_list = []
		clean_tweet_list = []
		time_list = []
		Vader_list = []
		for row in csvReader:
			data = row["Tweet_text"], row["Time"], row["Vader_compound"]
			tweet_list.append(data)

	for tweet in tweet_list:
		text = tweet[0]
		time = tweet[1]
		Vader_compound = tweet[2]
		#remove RT, &amp, hyperlinks: preserve U.S.
		text = re.sub(r'https.*', '', text)
		text = text.replace('&amp', '')
		text = text.replace('U.S.', 'usa')
		text = text.replace('RT', '')
		# split tweets into tokens by white space
		tokens = text.split()
		# make lower case
		tokens = [word.lower() for word in tokens]
	# Remove punctuation no roman alphabet words from each tweet, except for # and @
	# preserve numbers( use is aplha for just letters, is alnum for letters and numbers)
		tokens = ["".join(c for c in word if c.isalnum() or c=="#" or c=="@") for word in tokens ]
	# remove stop words
		content_word_tweet = [w for w in tokens if not w in stop_words]
		lemmatizer = WordNetLemmatizer()
		lemmatized_output = ' '.join([lemmatizer.lemmatize(w)for w in content_word_tweet])

		# print(lemmatized_output)
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
			# .add is a set function (creates a set), so it will only add 1 time, set values have to be unique
			except:
				DF[w] = {i}
	# the except adds the word if the word doesn't exist in the dictionary (creates a key and stores the first index)
	
	# print(DF.items())
	for word in DF:
		#get the number of occurences of each word
		DF[word] = len(DF[word])
		#extract the words with # and @
		if '#' in word:
			hashtags.append(word)
		if '@' in word:
			references.append(word)
	from collections import Counter
	number = Counter(references)
	print(f"sample references: {references[0:9]} sample hashtags {hashtags[0:9]}")
	print(f"There are {len(hashtags)} hashtags \nThere are {len(references)} references")
	sorted_frequency = sorted(DF.items(), key = lambda x: x[1], reverse = True)
#	remove the blank spaces at position 0
	print(f"The top 40 words are {sorted_frequency[1:40]}")
	# create a list of unique words
	total_vocab = [x for x in DF]
	print(f"There are {len(total_vocab)}  unique words after removing stop words")

word_counter()
