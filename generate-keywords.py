#! /usr/bin/env python3
from urllib.request import urlopen, Request
from pymongo import MongoClient
import textract
import os
import requests
import pandas as pd
from pprint import pprint
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from nltk.corpus import stopwords
from helper_functions import *
from bson.objectid import ObjectId

# mongoDB = os.environ['MONGO_DB']
mongoDB = 'mongodb://192.168.99.100/sedaily'
client = MongoClient(mongoDB)
db = client.get_database()
# posts = db.posts.find()

posts = requests.get(
    'http://192.168.99.100:4040/api/posts?transcripts=true&limit=500').json()

print(len(posts))

custom_stopwords = get_stopwords()

articles = pd.read_pickle('./pickle-files/preprocessed_docs.pkl')

print('length of articles', len(articles))

df_articles = pd.DataFrame(articles)

corpus = df_articles['full_text'].tolist()

vectorizer = TfidfVectorizer(
    max_df=0.85, smooth_idf=True, use_idf=True, stop_words=custom_stopwords)
X = vectorizer.fit_transform(corpus)

# get feature to index mapping
feature_names = vectorizer.get_feature_names()

# generate tf-idf for the given document
for post in posts:
    keywords = {}
    transcriptUrl = post['transcriptUrl']
    postId = post['_id']
    tags = post['filterTags']
    print('mongoDb _id', postId, '\n', 'tags: ', tags, '\n')
    (filename, text) = pre_process_transcript(transcriptUrl)
    os.remove(filename)

    tf_idf_vector = vectorizer.transform([text])

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    print('sorted', sorted_items[:30])
    # extract only the top n; n here is 10
    keywords = extract_topn_from_vector(feature_names, sorted_items, 30)
    for tag in tags:
        keywords[tag['slug']] = 1.0
    print('raw keywords', keywords)
    print("\n===Text===")
    print(filename, text)
    # now print the results
    print("\n===Keywords===")
    for k in keywords:
        print(k, keywords[k])
    try:
        db.posts.update({'_id': ObjectId(post['_id'])}, {'$set': { 'keywords': keywords }}, upsert=False, multi=False)
    except:
        print('failed to update')
    # db.close()
