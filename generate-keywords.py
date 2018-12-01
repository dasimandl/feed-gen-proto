import textract
import sys
import os
import requests
import pandas as pd
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from nltk.corpus import stopwords
sys.path.append("./utils")
from helper_functions import *
from pymongo import MongoClient
from urllib.request import urlopen, Request

# mongoDB = os.environ['MONGO_DB']
mongoDB = 'mongodb://192.168.99.100/sedaily'
client = MongoClient(mongoDB)
db = client.get_database()
# posts = db.posts.find()
posts = requests.get('http://192.168.99.100:4040/api/posts?transcripts=true&limit=3').json()

print(len(posts))
for post in posts:
  transcriptUrl = post['transcriptUrl']
  _id = post['_id']
  print(transcriptUrl, _id)
  print(pre_process_transcript(transcriptUrl))

# custom_stopwords = get_stopwords()

# articles = pd.read_pickle('./pickle-files/preprocessed_docs.pkl')

# print('length of articles', len(articles))

# df_articles = pd.DataFrame(articles)

# corpus = df_articles['full_text'].tolist()

# vectorizer = TfidfVectorizer(max_df=0.85, smooth_idf=True, use_idf=True,stop_words=custom_stopwords)
# X = vectorizer.fit_transform(corpus)

# # get feature to index mapping
# feature_names = vectorizer.get_feature_names()

# #generate tf-idf for the given document
# tf_idf_vector = vectorizer.transform([test])

# #sort the tf-idf vectors by descending order of scores
# sorted_items = sort_coo(tf_idf_vector.tocoo())
# print('sorted',sorted_items[:30])
# #extract only the top n; n here is 10
# keywords = extract_topn_from_vector(feature_names,sorted_items,20)
# print('raw keywords', keywords)
# # now print the results
# print("\n===Keywords===")
# for k in keywords:
#     print(k,keywords[k])
