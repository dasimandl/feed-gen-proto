#! /usr/bin/env python3
import re
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import pickle
import textract
import requests
from urllib.request import urlopen, Request, urlretrieve


lemma = WordNetLemmatizer()


def get_stopwords():
    with open('./utils/stopwords.txt') as f:
        additional_stopwords = f.read().splitlines()

    return set(stopwords.words('english') + list(additional_stopwords))


def save_obj(obj, name):
    with open('./pickle-files/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=20):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


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


def download_pdf(url):
    formattedUrl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(formattedUrl)
    filename = './tmp/' + url.split('/')[7]
    return save_pdf(response, filename)


def save_pdf(pdf, filename):
    file = open(filename, 'wb')
    file.write(pdf.read())
    file.close()
    return filename

def pre_process_transcript(url):
    filename = download_pdf(url)
    text = textract.process(filename, encoding='utf_8').decode('utf-8')
    text = text.replace('\n', ' ')
    text = text.replace('\n', ' ')
    text = text.lower()
    text = re.sub("(\\d|\\W|\\_)+", " ", text)
    text = re.sub(
        "software engineering daily|transcript|introduction", " ", text)
    text = re.sub('(sponsor message).*?(interview)', " ", text)
    text = re.sub('(end of interview).+', " ", text)
    tokens = word_tokenize(text)
    pos_tokens = pos_tag(tokens)
    lemmatized_tokens = [lemma.lemmatize(
        token[0], pos=get_wordnet_pos(token[1])) for token in pos_tokens]
    text = " ".join(
        word for word in lemmatized_tokens if word not in get_stopwords() and len(word) > 3)
    return filename, text
