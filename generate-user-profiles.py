#! /usr/bin/env python3
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
from functools import reduce

mongoDB = 'mongodb://192.168.99.100/sedaily'
client = MongoClient(mongoDB)
db = client.get_database()

users = db.users.find({})

for user in users:
    user_id = ObjectId(user['_id'])
    feature_vectors = []
    print(user_id)
    listeneds = db.listeneds.find({'userId': user_id})
    print(user['name'])

    for listened in listeneds:
        post_id = ObjectId(listened['postId'])
        posts = db.posts.find({'_id': post_id})
        for post in posts:
            try:
                feature_vectors.append(post['keywords'])
            except Exception as e:
                print(e, 'keywords doesnt exist using filterTags')
                keywords = {}
                for keyword in post['filterTags']:
                    keywords[keyword['slug']] = 1.0
                feature_vectors.append(keywords)

    df_feature_vectors = []
    for feature_vector in feature_vectors:
        data_frame = pd.DataFrame({
            'key': list(feature_vector.keys()),
            'value': list(feature_vector.values())
        })
        df_feature_vectors.append(data_frame)

    # print(df_feature_vectors)
    try:
        user_features = reduce(lambda left, right: pd.merge(left, right, on='key', how='outer'), df_feature_vectors)
        sum = user_features.sum(axis=1)
        user_features['sum'] = user_features.sum(axis=1)
        user_features['mean'] = user_features.mean(axis=1)
        user_profile = pd.DataFrame({'key': user_features['key'], 'value': sum}).sort_values('value', ascending=False)
        # print(user_features)
        print(user_profile)
    except Exception as e:
        print('error: ', e)
