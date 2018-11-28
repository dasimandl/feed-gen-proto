import textract
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
from nltk.corpus import stopwords
import sys
sys.path.append("./utils")
from helperFunctions import *

custom_stopwords = get_stopwords()

articles = pd.read_pickle('./pickle-files/preprocessed_docs.pkl')

print('length of articles', len(articles))

df_articles = pd.DataFrame(articles)

corpus = df_articles['full_text'].tolist()

vectorizer = TfidfVectorizer(max_df=0.85, smooth_idf=True, use_idf=True,stop_words=custom_stopwords)
X = vectorizer.fit_transform(corpus)

# get feature to index mapping
feature_names = vectorizer.get_feature_names()

#generate tf-idf for the given document
tf_idf_vector = vectorizer.transform([test])

#sort the tf-idf vectors by descending order of scores
sorted_items = sort_coo(tf_idf_vector.tocoo())
print('sorted',sorted_items[:30])
#extract only the top n; n here is 10
keywords = extract_topn_from_vector(feature_names,sorted_items,20)
print('raw keywords', keywords)
# now print the results
print("\n===Keywords===")
for k in keywords:
    print(k,keywords[k])
