import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

articles = pd.read_pickle('./pickle-files/preprocessed_docs.pkl')

print('length of articles', len(articles))

df_articles = pd.DataFrame(articles)

print(df_articles['full_text'][1])
# print(df_articles.dtypes)
