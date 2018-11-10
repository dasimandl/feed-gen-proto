import Algorithmia
import pickle
# import enumerate
algo_client = Algorithmia.client('sim5s5q8M4yVke97xO5CFiP08CF1')
algo = algo_client.algo('web/AnalyzeURL/0.2.17')

def save_obj (obj, name):
  with open('./pickle-files/' + name + '.pkl', 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj (name):
  with open('./pickle-files/' + name + '.pkl', 'rb') as f:
    return pickle.load(f)

articles = []
docs = []
try:
  articles = load_obj('hn_articles')
  print('loaded hn_articles', len(articles))
  print(articles[:10])
  for i, article in enumerate(articles):
    try:
      algo_response = algo.pipe(article["url"]).result
      # print(algo_response)
      # tokenized_text = tokenize(algo_response["text"].lower())
      docs.append({
        "title": article["title"],
        "url": article["url"],
        "text": algo_response["text"],
        "analyzed_url": algo_response,
        "date": article["date"],
        "hn_id": article["hn_id"]
      })
    except:
      print('error for: ', article["url"])
      continue

    if (i % 5 == 0):
      print(i, article["url"])

    if (i % 500 == 0):
      save_obj(docs, 'analyzed_articles')
      print('sved docs to file')

  save_obj(docs, 'analyzed_articles')
except:
  print('unable to load hn_articles.pkl')

