'''
Название, ник,карма, рейтинг, подписчики, состоит в хабах,
 количество публикаций, приглашен, колво комментов,
  закладок, активность, зарегистрирован, влакды в хабы (название балл) откуда 
'''


from bs4 import BeautifulSoup
import requests
import sys
import csv
import pprint
import os
import time
__URL_USERS__ = 'https://habrahabr.ru/users/'

__ATTRS_ = {
'name' : {'class' :'user-info__fullname user-info__fullname_medium'}
,'karma' : {'class' :'stacked-counter__value stacked-counter__value_green '}
,'rating' : {'class' :'stacked-counter__value stacked-counter__value_magenta'}
,'subs' : {'class' :'stacked-counter__value stacked-counter__value_blue'}
,'invited by' : {'class' : 'profile-section__invited'}
}
__ATTRS_TAG__ = ['published', 'comments', 'tabs']
__ATTR__INFO__=  'defination-list__item defination-list__item_profile-summary'
__ATTR_CONTR__ = 'media-obj__body media-obj__body_hub'
__ATTR_POSTS__ = 'post__title_link'
__ATTR_HUBCONSIST__ = 'profile-section__user-hub '

def getPubCommTags(text, currentUser):
	#print(text)
	t = text.findAll(attrs= {'class' : 'tabs-menu__item-counter tabs-menu__item-counter_total'})
	try:
		for i in range(0, 3):
			currentUser.addData(__ATTRS_TAG__[i], t[i].text)
	except Exception:
		pass


def getHubIncludes(text, currentUser):
	hubs = text.findAll(attrs= {'class' : __ATTR_HUBCONSIST__})
	incl = []
	try :
		for i in hubs:
			incl.append(i.text)
	except Exception: 
		pass

	currentUser.addData('hubIncludes', incl)

def getHubContrib(text, currentUser):
	hubs = text.findAll(attrs= {'class' : __ATTR_CONTR__})
	ratingHubs = []
	try : 
		for i in hubs:
			title = i.find(attrs = {"class" : 'rating-info__title'}).text
			score = i.find(attrs = {"class" : 'rating-info__stat'}).text
			ratingHubs.append((title, score))
	except Exception: 
		pass
	currentUser.addData('hubsContribution', ratingHubs)
def getPublications(currentUser):
	text = BeautifulSoup(requests.get(__URL_USERS__ + currentUser.nickname() + '/posts').text, 'html.parser')
	posts = []
	for i in text.findAll(attrs = {'class' : 'post__title_link'}):
		#currentPost = Post(i.attrs['href'], i.text)
		posts.append((i.attrs['href'], i.text))
	currentUser.addData('Posts', posts)

def getInfo(text, currentUser):
	hubs = text.findAll(attrs= {'class' : __ATTR__INFO__})
	info = []
	try : 
		for i in hubs:
			title = i.find(attrs = {"class" : 'defination-list__label defination-list__label_profile-summary'}).text		
			value = i.find(attrs = {"class" : 'defination-list__value'}).text
			info.append((title, value))

	except Exception as e: 
		pass

	currentUser.addData('information', info)


class User():
	def __init__(self, nickname):
		self.data = {'nickname':nickname}
	def addData(self, key, val = 'no data'):
		self.data[key] = val
	def nickname(self):
		return self.data['nickname']
	def __str__(self):
		return str(self.data.items())
	def printer(self):
		#pprint.pprint(self.data)
		logFile = 'logs.txt'
		if os.path.exists(logFile):
			param = 'a'
		else:
			param = 'w'

		logFile=open('logs.txt', param)
		pprint.pprint(self.data, stream = logFile)
		pprint.pprint('------------------------------------------------------------------------------------------',
			stream = logFile)
		logFile.close()


class Post():
	def __init__(self, link, name):
		self.link = link
		self.name = name
	def __str__(self):
		return str(self.name + " " + self.link)

def parseUser(nickname):
	response = requests.get(__URL_USERS__ + nickname)
	#if (response.status_code != 200):
	print(response.status_code)
	text = BeautifulSoup(response.text, 'html.parser')
	currentUser = User(nickname)
	for i in __ATTRS_.items():
		try:
			data = (text.find(attrs = i[1])).text
			currentUser.addData(i[0], ' '.join(data.split()))
		except Exception as e:
			pass
		
	getPubCommTags(text, currentUser)
	getHubContrib(text, currentUser)
	getInfo(text, currentUser)
	getPublications(currentUser)
	getHubIncludes(text, currentUser)
	#print(currentUser)
	currentUser.printer()


def parse():
	text = BeautifulSoup(requests.get(__URL_USERS__).text, 'html.parser')
	users = []
	numberOfUser = 1
	print(time.clock())
	for i in text.findAll(attrs= {'class' : 'list-snippet__nickname'}):
		parseUser(i.text)
		print(numberOfUser)		
		numberOfUser += 1
		#print(time.clock())

if (__name__ == '__main__'):
	parse()
	#parseUser('aaaa')