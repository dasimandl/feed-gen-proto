from hackernews import HackerNews
from pymongo import MongoClient
from urllib.request import urlopen
from nltk.stem import WordNetLemmatizer
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from heapq import nlargest
import nltk
import gensim
from gensim import corpora, models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from pprint import pprint
import Algorithmia
import json
import pprint
import urllib
import pickle

client = MongoClient('mongodb://192.168.99.100')
db = client['sedaily']

hn = HackerNews()

algo_client = Algorithmia.client('sim5s5q8M4yVke97xO5CFiP08CF1')
algo = algo_client.algo('web/AnalyzeURL/0.2.17')

vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')

# print(top_stories)

additionalStopWords = ["'ve", "'s", "'ll", "'nt", "'d"]
customStopWords = set(stopwords.words('english') + list(punctuation) + list(additionalStopWords))
# print ("CUSTOM STOP", customStopWords)

articles = []
# print(vars(top_stories[0]))
# test url https://developers.google.com/web/updates/2018/10/wasm-threads

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def tokenize (text):
  clean_tokens = [token for token in word_tokenize(text) if token not in customStopWords]
  return clean_tokens

try:
  articles = load_obj('articles')
  print('loaded articles from file', len(articles))
except FileNotFoundError:
  top_stories = hn.top_stories(limit=1000)
  print('pulled top stories', len(top_stories))
  for story in top_stories:
    print(story.url)
    try:
      algo_response = algo.pipe(story.url).result
      tokenized_text = tokenize(algo_response["text"].lower())
      articles.append({
        "title": story.title,
        "url": story.url,
        "text": algo_response['text'],
        "tokenized_text": tokenized_text,
        "algo_response": algo_response,
        "hn": story
      })
    except:
      print('error for: ', story.url)
    # tokenized_text = (algo_response["text"])
  save_obj(articles, 'articles')

# print(articles[0]["tokenized_text"])
text = [article["text"] for article in articles]

vectorizer = TfidfVectorizer(max_df=0.5,min_df=2,stop_words='english')
print('vectorizing')
X = vectorizer.fit_transform(text)
print('shape',X.shape)
X[0]
X

from sklearn.cluster import KMeans
km = KMeans(n_clusters = 3, init = 'k-means++', max_iter = 100, n_init = 1, verbose = True)
km.fit(X)

import numpy as np
print(np.unique(km.labels_, return_counts=True))

docs={}
for i,cluster in enumerate(km.labels_):
    oneDocument = text[i]
    if cluster not in docs.keys():
        docs[cluster] = oneDocument
    else:
        docs[cluster] += oneDocument

print(len(docs))

keywords = {}
counts={}

for cluster in range(3):
    word_sent = word_tokenize(text[cluster].lower())
    word_sent=[word for word in word_sent if word not in customStopWords]
#     print(word_sent)
    freq = FreqDist(word_sent)
    # pprint(freq)
    keywords[cluster] = nlargest(100, freq, key=freq.get)
    counts[cluster]=freq

print(keywords)
unique_keys={}
for cluster in range(3):
    other_clusters=list(set(range(3))-set([cluster]))
    keys_other_clusters=set(keywords[other_clusters[0]]).union(set(keywords[other_clusters[1]]))
    unique=set(keywords[cluster])-keys_other_clusters
    unique_keys[cluster]=nlargest(10, unique, key=counts[cluster].get)

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=3)
classifier.fit(X,km.labels_)

# article = "Facebook Inc. has been giving advertisers an inflated metric for the average time users spent watching a video, a measurement that may have helped boost marketer spending on one of Facebook’s most popular ad products. The company, owner of the world’s largest social network, only counts a video as viewed if it has been seen for more than 3 seconds. The metric it gave advertisers for their average video view time incorporated only the people who had watched the video long enough to count as a view in the first place, inflating the metric because it didn’t count anyone who didn’t watch, or watched for a shorter time. Facebook’s stock fell more than 1.5 percent in extended trading after the miscalculation was earlier reported in the Wall Street Journal. Facebook had disclosed the mistake in a posting on its advertiser help center web page several weeks ago. Big advertising buyers and marketers are upset about the inflated metric, and asked the company for more details, according to the report in the Journal, citing unidentified people familiar with the situation. The Menlo Park, California-based company has kept revenue surging in part because of enthusiasm for its video ads, which advertisers compare in performance to those on Twitter, YouTube and around the web."

 article =  "In the past four years, I’ve been working as an engineering manager. First, as the co-founder of RisingStack, then Godaddy and now Uber. In all of these cases, I was and am between the tech lead engineering manager and the people engineering manager. This article summarizes a few lessons learned, as well as shows you how I manage to work on code. Hopefully it gives you a few ideas to adopt too, if you are an engineering manager with an appetite for coding. If you’d like to learn more on these types of engineering managers, I’d recommend reading Benjamin Encz’s Flavors of Engineering Management. As an engineering manager I found code reviews tremendously helpful for not just ensuring quality across the codebase, but because of its knowledge sharing nature. I look at code reviews more as a broadcasting channel for the changes applied to the code base rather than a way of ensuring quality. As an engineering manager, code reviews are a great way to: If you’d like to and still have the time to work on the codebase sometimes, I’d highly recommend picking bug fixes or small features. Bug fixes let you dive into the breadth and the depth of the codebase and understand how it works, while also contributing back something useful to the team. With features, I’d be more cautious. Your schedule is sometimes unpredictable, as you might be getting pulled into meetings unexpectedly, so you can easily end up blocking your team. If you live in an area where there are coding schools / community-driven mentoring sessions around you, and you have the time to attend, I’d give that a try! Depending on the format, it can be teaching or pair programming, with a lot of explaining on why things work in a given way. To look for mentoring events, give meetup.com a try! If you are involved in the JavaScript / Node.js space, I’d recommend checking out NodeSchool, which is a global workshop series dedicated to teach newcomers JavaScript and Node.js. It also worked great for me to work on open-source projects either as a maintainer or a contributor. Back at my days at Godaddy, I’ve started Terminus, a Node.js library dealing with graceful shutdowns and health checks, and I’ve kept maintaining it ever since. It is a great way to stay up-to-date with both Node.js and Kubernetes through incoming pull requests and issues, as the library build on those technologies. If you’d like to do something similar, but you don’t have a project, I’d recommend searching for the labels “help wanted” or “good first issue” on GitHub to get involved with a project. To stay with the example at Node.js, you can take a look at the issues labeled with “good first issue” using this link. Depending on what flavour of engineering management you are practicing, you may have the chance to work on code once in while. If you do, keep in mind to pick tasks that are small and not time sensitive, so you won’t block your team. Did I miss anything  What are you doing to keep in touch with coding as an engineering manager  Please let me know in the comments below!",




test=vectorizer.transform([article])

# print(test)
print(unique_keys)
print(classifier.predict(test))
# freq = FreqDist(articles[5]["tokenized_text"])
# top20 = nlargest(50, freq, key=freq.get)
# top20 = [{term: freq[term]} for term in top20 ]

# print(top20)
# print(articles[5]['url'])
# print(articles[0]["tokenized_text"])
# print(articles[0]["url"])
# print(articles[0]["tokenized_text"])


