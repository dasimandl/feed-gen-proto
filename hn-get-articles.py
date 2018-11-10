from hackernews import HackerNews
from urllib.request import urlopen
import pickle

def save_obj (obj, name):
  with open('./pickle-files/' + name + '.pkl', 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj (name):
  with open('./pickle-files/' + name + '.pkl', 'rb') as f:
    return pickle.load(f)

hn = HackerNews()

hn_items = []
index = 0

try:
  hn_id = load_obj('last_hn_id')
  print('loaded id:', hn_id)
except:
  hn_id = hn.get_max_item()
  print('max_id from hn:', hn_id)

while len(hn_items) < 5:
  index += 1
  try:
    item = hn.get_item(hn_id)
  except:
    print('hn_id invalid', hn_id)
    hn_id -= 1
    continue
  # print('item', type(item))
  if item.item_type == "story" and item.url is not None:
    if len(hn_items) % 5 == 0:
      print(len(hn_items))
    hn_items.append({"url": item.url, "hn_id": item.item_id, "date": item.submission_time, "title": item.title})
  hn_id -= 1

try:
  articles = load_obj('hn_articles')
  print('articles file loaded length', len(articles))
  articles = articles + hn_items
  print('articles appended hn_items', len(articles))
except:
  print('unable to load existing articles file')
  articles = hn_items

try:
  save_obj(articles, 'hn_articles')
  print('hn_articles saved')
except:
  print('unable to save articles')

print("last id", hn_id)
try:
  save_obj(hn_id,'last_hn_id')
  print('saved last hn_id:', hn_id)
except:
  print('unable to save hn_id:', hn_id)

print("i", index, len(articles))
# print('articles', articles)
