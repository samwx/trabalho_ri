# -*- coding: utf-8 -*-
from instagram.client import InstagramAPI
import sys, requests, json

class InstagramHandler:
	def __init__(self):
		self._client_id = 'b227fdb586e94471a4c4d15adc51f947'
		self._client_secret = '9e4a2a7cc0b44f7286226b66ade71e12'
		self._code = '766e0cb3c06746038f0a0562035bf509'
		self._redirect_uri = 'http://samuelmartins.me'
		self._access_token = '33406230.b227fdb.4828b7b3470b4a23b9459f2aabbede35'

	"""
	Método para buscar as fotos/vídeos com a hashtag/palavra e o número de resultados passados via parâmetro
	"""
	def getRecentHashtagMedia(self, hashtag, count):
		requestedUrl = 'https://api.instagram.com/v1/tags/'+ hashtag +'/media/recent?access_token='+ self._access_token +'&count=' + str(count)
		req = requests.get(requestedUrl)
		instagramMedias = json.loads(req.text)
		arrInstagram = {"results": []}

		for media in instagramMedias['data']:
			if media['caption']:
				mediaText = media['caption']['text']

			singleMedia = {
				"profile_name": media['user']['full_name'],
				"user_name": media['user']['username'],
				"image": media['images']['low_resolution']['url'],
				"link": media['link'],
				"tags": media['tags'],
				"text": mediaText,
				"category": ''
			}

			arrInstagram['results'].append(singleMedia)

		return arrInstagram
