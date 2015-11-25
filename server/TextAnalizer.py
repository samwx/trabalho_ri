# -*- coding: utf-8 -*-
import collections, sys
from NegativeLayer import *
from PositiveLayer import *

class TextAnalizer:

	"""Palavras mais frequentes do documento"""
	def mostCommon(self, content):
		cnt = collections.Counter()

		for phrase in content:
			arrTxt = phrase['phrase'].split(' ')

			for word in arrTxt:
				cnt[word] += 1

		return cnt.most_common(5)

	"""Faz uma interseção com a lista de stopwords e lista de palavras"""
	def sanitizePhrase(self, user_input, hashtag):
		stopWordsFile = open('stopwords.txt', 'r')
		stopWordsList = stopWordsFile.read().split()
		stopWordsFile.close()

		#Adiciona à lista de stop words a hashtag buscada
		#Obviamente, ela será a palavra mais frequente
		stopWordsList.append(hashtag.lower())
		stopWordsList.append('#'+hashtag.lower())
		stop_words = set(stopWordsList)
		user_input = user_input.lower().split()

		for sw in stop_words.intersection(user_input):
			while sw in user_input:
				user_input.remove(sw)

		points = self.classifyPhraseWithPoints(user_input)

		info = {
			"phrase": ' '.join(user_input),
			"points": points
		}

		return info

	"""
	Classifica a frase fazendo uma interseção das palavras com a lista de palavras
	positivas e negativas
	"""
	def classifyPhraseWithPoints(self, inputWords):
		points = 0
		inputWords = set(inputWords)

		negativeLayer = NegativeLayer()
		positiveLayer = PositiveLayer()

		negativeWords2 = negativeLayer.listWeight2
		negativeWords1 = negativeLayer.listWeight1

		positiveWords2 = positiveLayer.listWeight2
		positiveWords1 = positiveLayer.listWeight1

		"""
		Para cada palavra no documento, o loop verifica se esta palavra está contida em alguma das listas de "palavras com sentimento".
		Caso ela esteja em alguma lista, é adicionado uma pontuação ao documento de acordo com o peso da lista em que a palavra está presente.
		Se ela não estiver nas listas (digitação errada), é encontrado em qual dessas listas existe uma palavra que é a mais próxima da palavra digitada
		e é adicionado uma pontuação proporcional à distância de levenshtei e ao peso da lista. Quanto maior a distância, menor a pontuação.
		"""
		for word in inputWords:
			nearestWord = [0,sys.maxint]

			for sentimentWord in negativeWords2["words"]:
				if word == sentimentWord:
					points = points - 2
				elif nearestWord[1] > 1:
					proximity = self.levenshteinDistance(word, sentimentWord)
					if proximity < nearestWord[1] and proximity <= 3:
						nearestWord[0] = 1
						nearestWord[1] = proximity

			for sentimentWord in negativeWords1["words"]:
				if word == sentimentWord:
					points = points - 1
				elif nearestWord[1] > 1:
					proximity = self.levenshteinDistance(word, sentimentWord)
					if proximity < nearestWord[1] and proximity <= 3:
						nearestWord[0] = 2
						nearestWord[1] = proximity

			for sentimentWord in positiveWords2["words"]:
				if word == sentimentWord:
					points = points + 2
				elif nearestWord[1] > 1:
					proximity = self.levenshteinDistance(word, sentimentWord)
					if proximity < nearestWord[1] and proximity <= 3:
						nearestWord[0] = 3
						nearestWord[1] = proximity

			for sentimentWord in positiveWords1["words"]:
				if word == sentimentWord:
					points = points + 1
				elif nearestWord[1] > 1:
					proximity = self.levenshteinDistance(word, sentimentWord)
					if proximity < nearestWord[1] and proximity <= 3:
						nearestWord[0] = 4
						nearestWord[1] = proximity

			if nearestWord[0] != 0 and nearestWord[1] != sys.maxint:
				if nearestWord[0] == 1 : weight = -2
				if nearestWord[0] == 2 : weight = -1
				if nearestWord[0] == 3 : weight = 2
				if nearestWord[0] == 4 : weight = 1
				points = points + (float(weight)/float(nearestWord[1]) + float(0.5))

		return points

	"""
	Utiliza o algoritimo de Levenshtein "Distância de edição" para tentar corrigir
	um possível erro de digitação nas palavras
	"""
	def levenshteinDistance(self, s1, s2):
		if len(s1) > len(s2):
			s1, s2 = s2, s1

		distances = range(len(s1) + 1)
		for i2, c2 in enumerate(s2):
			distances_ = [i2+1]
			for i1, c1 in enumerate(s1):
				if c1 == c2:
					distances_.append(distances[i1])
				else:
					distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
			distances = distances_
		return distances[-1]

