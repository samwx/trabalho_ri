# -*- coding: utf-8 -*-
import tweepy
from TextAnalizer import *

class TwitterHandler:
    def __init__(self):
        self._consumer_key = "JYTLIYsfezyCzuyGfyvr2CFVb"
        self._consumer_secret = "F0An03giFcaLq26tV3i2VrL2TUl00yNmvriYX2PhpXqqIPqL9Q"
        self._access_key = "132556025-5SIFeLNTV29yFsn6MJzDwUbKlUR2XsQV2fW3rnFX"
        self._access_secret = "YsEt41KyUxcQnm2nQ5z5RsZuk0gGR6AXW8X2y6a1DOq7V"

        #Array com os dados de acesso a API
        self._OAUTH_KEYS = {
            'consumer_key'        : self._consumer_key,
            'consumer_secret'     : self._consumer_secret,
            'access_token_key'    : self._access_key,
            'access_token_secret' : self._access_secret
        }

    """
    Autentica o usuário para fazer as requisições na API
    """
    def startAuth(self):
        auth = tweepy.OAuthHandler(self._OAUTH_KEYS['consumer_key'], self._OAUTH_KEYS['consumer_secret'])
        api = tweepy.API(auth)
        return api

    """
    Método para buscar os tweets com a hashtag/palavra e o número de resultados passados via parâmetro
    """
    def getHashtagTweets(self, hashtag, count):
        twitter_api = self.startAuth()
        myTweets = tweepy.Cursor(twitter_api.search, q='#'+hashtag, lang="pt",
            locale="pt").items(count)
        arrTweets = {"results": []}

        #Loop for tweets results
        for tweet in myTweets:
            tweetStatus = tweet.text.encode(encoding='UTF-8',errors='strict')
            tweetUser = tweet.user.screen_name
            tweetProfile = tweet.user.name

            singleTweet = {
                "profile_name": tweetProfile,
                "user_name": tweetUser,
                "tweet": tweetStatus,
                "category": ''
            }

            arrTweets['results'].append(singleTweet)

        return arrTweets


