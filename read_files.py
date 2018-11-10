import pandas as pd

articles = pd.read_pickle('analyzed_articles.pkl')

print('length of articles', len(articles))

df_articles = pd.DataFrame(articles)

print(df_articles['title'][1])
