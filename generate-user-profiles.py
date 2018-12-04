#! /usr/bin/env python3
from pymongo import MongoClient
from bson.objectid import ObjectId

mongoDB = 'mongodb://192.168.99.100/sedaily'
client = MongoClient(mongoDB)
db = client.get_database()

users = db.users.find({})

for user in users:
    userFeatures = []
    userId = ObjectId(user['_id'])
    print(userId)
    listeneds = db.listeneds.find({'userId': userId})
    for listened in listeneds:
        postId = ObjectId(listened['postId'])
        posts = db.posts.find({'_id': postId})
        print(user['name'])
        for post in posts:
            try:
                print(post['keywords'].keys())
            except Exception as e:
                print(e, 'keywords doesnt exist using filterTags')
                keywords = {}
                for keyword in post['filterTags']:
                    keywords[keyword['slug']] = 1.0
                print(keywords.keys())
