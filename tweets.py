import pymongo
from pymongo import MongoClient
import json
import twitter
from pprint import pprint
from abc import ABCMeta,abstractmethod

class TwitterConfig:

    __CONSUMER_KEY = "22XFA1jHP4VTUEmEyhiGUtD80"
    __CONSUMER_SECRET = "UmYCo8IZ12NJ84iu4dH6wEAGXbNzEvUf9HV4PzG5aTxhTh3CIp"
    __OAUTH_TOKEN = "981633761786974208-g628s2L3TmBe7UD4jHBs8VoiIDISfun"
    __OAUTH_TOKEN_SECRET = "X1mxrhXbecXnhYfrCw9UU1kLGdDT0SY3XKRYUkvknUrlI"

class twitterBase(metaclass=ABCMeta):

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

class MongoInitilize(twitterBase,TwitterConfig):


    def callApi(self):
        self.auth = twitter.oauth.OAuth(self._TwitterConfig__OAUTH_TOKEN, self._TwitterConfig__OAUTH_TOKEN_SECRET, self._TwitterConfig__CONSUMER_KEY, self._TwitterConfig__CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)
        return self.twitter_api

    def startProcess(self):
        self.client = MongoClient()
        self.db = self.client.tweets_db
        self.tweet_collection = self.db.tweet_collection
        self.tweet_collection.create_index([("id",pymongo.ASCENDING)],unique=True)
        print("Database Created")
        self.searchTweets()

    def searchTweets(self):
        print("Searching tweets")
        self.count = 50
        self.query = "Trump"
        self.tweetz = self.callApi()
        self.searchResult = self.tweetz.search.tweets(count=self.count,q=self.query)
        pprint(self.searchResult['search_metadata'])
        self.saveTweets()

    def saveTweets(self):
        print("Saving the tweets into mongoDB")
        self.statuses = self.searchResult["statuses"]
        for status in self.statuses:
            try:
                self.tweet_collection.insert(status)
            except:
                pass

if __name__ == '__main__':
    mongo = MongoInitilize()
    mongo.startProcess()
