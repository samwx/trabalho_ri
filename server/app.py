# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask.ext.cors import CORS
from TwitterHandler import *
from InstagramHandler import *
from TextAnalizer import *
import tweepy, json, sys, requests

reload(sys)
sys.setdefaultencoding('utf8')

#Flask local server
app = Flask(__name__)
CORS(app)

#Twitter authenticate and attributes
twitterHandler = TwitterHandler()

#Instagram auth and attributes
instagramHandler = InstagramHandler()

#Twitter routes
@app.route('/api/twitter/<hashtag>/<int:count>', methods=['GET'])
def showTweets(hashtag, count):
	tweets = twitterHandler.getHashtagTweets(hashtag, count)

	return json.dumps(tweets, ensure_ascii=False, indent=2)

#Instagram routes
@app.route('/api/instagram/<hashtag>/<int:count>', methods=['GET'])
def showInstagramMedia(hashtag, count):
	instagramMedia = instagramHandler.getRecentHashtagMedia(hashtag, count)

	return json.dumps(instagramMedia, ensure_ascii=False, indent=2)

#Global search route
@app.route('/api/search/<hashtag>/<int:count>', methods=['GET'])
def searchFormatedResults(hashtag, count):
	#JSON com os resultados originais das redes sociais
	results = {
		"twitter" : [],
		"instagram" : [],
		"frequentlyWords" : [],
		"approval": []
	}

	#Lista para todas as frases de twitter e instagram
	txtAux = []

	#Resultados instagram
	instagramMedia = instagramHandler.getRecentHashtagMedia(hashtag, count)

	#Resultados twitter
	tweets = twitterHandler.getHashtagTweets(hashtag, count)

	results['twitter'] = tweets
	results['instagram'] = instagramMedia

	#Text Analizer object
	txtAnalizer = TextAnalizer()

	for tweet in results['twitter']['results']:
		phrase = tweet['tweet'].encode(encoding='UTF-8',errors='strict')
		infos = txtAnalizer.sanitizePhrase(phrase, hashtag)
		txtAux.append(infos)
		tweet['category'] = 'negative' if infos['points'] < 0 else 'positive'

	for media in results['instagram']['results']:
		if media['text'] :
			phrase = media['text'].encode(encoding='UTF-8',errors='strict')
			infos = txtAnalizer.sanitizePhrase(phrase, hashtag)
			txtAux.append(infos)
			media['category'] = 'negative' if infos['points'] < 0 else 'positive'

	#Verifica as palavras mais frequentes em cada frase
	results['frequentlyWords'] = txtAnalizer.mostCommon( txtAux )

	#Faz a porcentagem das palavras positivas e negativas
	positivePhrases = 0
	negativePhrases = 0

	for phrase in txtAux:
		if phrase['points'] > 0:
			positivePhrases += 1
		if phrase['points'] < 0:
			negativePhrases += 1

	approvalInfos = {
		'negative' : negativePhrases,
		'positive' : positivePhrases
	}

	results['approval'].append(approvalInfos)

	return json.dumps(results, ensure_ascii=False, indent=2)

@app.route('/api/words', methods=['GET'])
def wordsWithWeights():
	file = open('negative.txt', 'r')
	contents = file.read()
	file.close()

	words = {
		"weight": 1,
		"words" : []
	}

	for word in contents.split():
		words["words"].append(word)

	return json.dumps(words, ensure_ascii=False, indent=2)


#Flask server
if __name__ == '__main__':
	app.run(debug=True)
