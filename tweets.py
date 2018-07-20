import pymongo
from pymongo import MongoClient
import json
import twitter
from pprint import pprint
from abc import ABCMeta,abstractmethod
from twiterKeys import TwitterConfig


class TwitterBase(metaclass=ABCMeta):

    @abstractmethod
    def callApi(self):
        return 0
    @abstractmethod
    def startProcess(self):
        return 0
    @abstractmethod
    def searchTweets(self):
        return 0
    @abstractmethod
    def saveTweets(self):
        return 0

class MongoInitilize(TwitterBase,TwitterConfig):

    ## api call to fetch tweets from twitter
    def callApi(self):
        self.auth = twitter.oauth.OAuth(self._TwitterConfig__OAUTH_TOKEN, self._TwitterConfig__OAUTH_TOKEN_SECRET, self._TwitterConfig__CONSUMER_KEY, self._TwitterConfig__CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)
        return self.twitter_api

    ## create data base using pymongo
    def startProcess(self):
        self.client = MongoClient()
        #print(self.client.list_database_names())
        ## check if data base already exists or not
        self.dbNames = self.client.list_database_names()
        if 'tweets_db' in self.dbNames:
            pass
        else:
            ## create our database
            self.db = self.client.tweets_db
            self.tweet_collection = self.db.tweet_collection
            self.tweet_collection.create_index([("id",pymongo.ASCENDING)],unique=True)
            print("Database Created")
        ## method call to perform the action
        self.searchTweets()

    def searchTweets(self):
        print("Searching tweets")
        self.count = 50
        self.query = "Trump"
        ## twitter api call
        self.tweetz = self.callApi()
        self.searchResult = self.tweetz.search.tweets(count=self.count,q=self.query)
        pprint(self.searchResult['search_metadata'])
        ## method call save the result into mongoDB
        self.saveTweets()

    def saveTweets(self):
        print("Saving the tweets into mongoDB")
        self.statuses = self.searchResult["statuses"]
        for status in self.statuses:
            try:
                self.tweet_collection.insert(status)
                ##pprint(status)
            except:
                pass

class PerformSentimentAnalysis(MongoInitilize):

    def __init__(self):
        self.client = MongoClient()
        self.dbNames = self.client.list_database_names()

    def checkData(self):
        if "tweets_db" in self.dbNames:
            self.db = self.client.tweets_db
            try:
                self.tweet_collection = self.db.tweet_collection
                self.tweet_cursor = self.tweet_collection.find()

                for document in self.tweet_cursor:
                    try:
                        print('-----')
                        print('name:-', document["user"]["name"])
                        print('text:-', document["text"])
                        print('Created Date:-', document["created_at"])
                    except:
                        print("Error in Encoding")
                        pass
            except:
                print("Documents not found")
                pass
        else:
            print("Database not found")

if __name__ == '__main__':
    mongo = MongoInitilize()
    mongo.startProcess()
    sanalysis = PerformSentimentAnalysis()
    sanalysis.checkData()
