
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import json
import string
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)

#import standard stopwords from NLTK, may need to customize this list
search_term = input("Please enter a search term:\n")
search_term = search_term.lower()

stop_words = set(stopwords.words('english'))
# import the json file and extract the text entries
with open('json/trumptweets.json', 'r') as f:
	trump_dict = json.load(f)
	trump_tweet_list = []
	for tweet in trump_dict:
		data = tweet["text"], tweet["created_at"]
		trump_tweet_list.append(data)
# clean the text
	clean_tweet_list = []
	total_tokens = 0
 	#remove hyperlinks
	for tweet in trump_tweet_list:
		text = tweet[0]
		time = tweet[1]
		text = re.sub(r'https.*', ' ', text)
	# split tweets into tokens by white space

		tokens = text.split()
	# remove punctuation from each tweet
		table = str.maketrans('', '', string.punctuation)
		tokens = [w.translate(table) for w in tokens]
	# remove remaining tokens that are not alphabetic
		tokens = [word for word in tokens if word.isalpha()]
	# make lower case
		tokens = [word.lower() for word in tokens]
	# searching for user input term
		if search_term in tokens:
			clean_tweet_list.append(tokens)
	user_text = clean_tweet_list
	# calculate the number of tokens
	number_of_tokens = len(user_text)
	print(f"There were {len(user_text)} tweets with the search term {search_term}")
print(user_text)