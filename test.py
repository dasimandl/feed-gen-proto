from hackernews import HackerNews
import nltk
import textract

hn = HackerNews()

# print(hn.top_stories(limit=10))
text = textract.process('./SED702-BloxRoute-Scaling-Bitcoin.pdf', encoding='utf_8').decode('utf-8')
text = text.replace('\n', ' ')
# print(len(text))
print(text)
tokens = nltk.word_tokenize(text)
print(tokens)
# print(type(text) is str)