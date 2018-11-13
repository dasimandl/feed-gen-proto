# from hackernews import HackerNews
import nltk
import textract
import re
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

with open('./utils/stopwords.txt') as f:
  additional_stopwords = f.read().splitlines()

custom_stopwords = set(stopwords.words('english') + list(additional_stopwords))

lemma = WordNetLemmatizer()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return wn.VERB



def pre_process (text):
  text = text.lower()
  text = re.sub("(\\d|\\W|\\_)+"," ",text)
  text = re.sub("software engineering daily|transcript|introduction|end of interview"," ",text)
  text = re.sub('(sponsor message).*?(interview)'," ",text)
  tokens = word_tokenize(text)
  pos_tokens = pos_tag(tokens)
  lemmatized_tokens = [lemma.lemmatize(token[0], pos=get_wordnet_pos(token[1])) for token in pos_tokens]
  text = " ".join(word for word in lemmatized_tokens if word not in custom_stopwords and len(word) > 3)
  return text
# hn = HackerNews()

# print(hn.top_stories(limit=10))
text = textract.process('./SED712-Mapillary-Research.pdf', encoding='utf_8').decode('utf-8')
text = text.replace('\n', ' ')
text = pre_process(text)
# print(len(text))
print(text)
# tokens = nltk.word_tokenize(text)
# print(tokens)
# print(type(text) is str)
