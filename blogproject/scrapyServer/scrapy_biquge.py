#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#python scrapy_biquge.py

from bs4 import BeautifulSoup
import requests
import json


baseUrl = "https://www.biduo.cc"


def search_request(url, param):
	
	try:

		if len(url) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})
		elif len(param['keyword']) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})

		searchUrl = 'https://www.biduo.cc/search.php'

		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		r = requests.get(url=searchUrl, headers=headers, params={'keyword': param['keyword']})
		soup = BeautifulSoup(r.text, features="html.parser")

		bookArray = list()

		total = '1'

		resultList = soup.select('.result-list .result-item')

		for result in resultList:

			detail = result.select('.result-game-item-detail')[0]
			title = detail.select('h3 a span')[0].string
			url = detail.select('h3 a')[0].attrs['href']
			intro = detail.select('p')[0].string

			info = detail.select('.result-game-item-info-tag')
			author = info[0].select('span')[1].string
			category = info[1].select('span')[1].string
			lastTime = info[2].select('span')[1].string
			newChapter = info[3].select('a')[0].string
			newUrl = info[3].select('a')[0].attrs['href']

			icon = result.select('.result-game-item-pic a img')[0].attrs['src']

			author = author.replace("\r\n", "")
			author = author.replace(" ", "")

			'''
			print('《%s》:%s' % (title, url))
			print('封面:%s' % icon)
			print('作者:%s' % author)
			print('%s:%s' % (newChapter, newUrl))
			print('分类:%s' % category)
			print('更新时间:%s' % lastTime)
			print('简介:%s' % intro)
			'''

			d = {"title": title, "url": url, "newChapter": newChapter, "newUrl": newUrl, "author": author, "lastTime": lastTime, "category": category, "intro": intro, "iconUrl": icon}
			bookArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"total": total, "bookArray": bookArray}})

	except requests.ConnectionError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except requests.HTTPError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except Exception as e:
		
		error = 'biquge_search_request：' + str(e)
		raise Exception(error)


def base_request(url):

	try:
		
		if len(url) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})

		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		r = requests.get(url=url, headers=headers).text
		r = r.encode("iso-8859-1").decode('gbk').encode('utf8')
		soup = BeautifulSoup(r, features="html.parser")

		return soup

	except requests.ConnectionError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except requests.HTTPError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except Exception as e:
		
		error = 'biquge_base_request：' + str(e)
		raise Exception(error)
	else:

		pass
	finally:

		pass


def category_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:

			return soup

		bookList = soup.select('#newscontent .l ul li')
		total = "1"

		bookArray = list()

		for book in bookList:

			title = book.select('.s2 a')[0].string
			url = book.select('.s2 a')[0].attrs['href']
			newChapter = book.select('.s3 a')[0].string
			newUrl = book.select('.s3 a')[0].attrs['href']
			author = book.select('.s5')[0].string
			intro = newChapter

			completeUrl = baseUrl + url
			completeNewUrl = baseUrl + newUrl

			'''
			print('《%s》:%s' % (title, completeUrl))
			print('%s:%s' % (newChapter, completeNewUrl))
			print('作者:%s' % author)
			'''

			d = {"title": title, "url": completeUrl, "newChapter": newChapter, "newUrl": completeNewUrl, "author": author, "intro": intro}
			bookArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"total": total, "bookArray": bookArray}})

	except Exception as e:
		
		error = 'biquge_category_request：' + str(e)
		raise Exception(error)


def chapter_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:
			
			return soup

		chapterList = soup.select('#list dl dd a')

		chapterArray = list()

		for chapter in chapterList:

			title = chapter.string
			chapterUrl = chapter.attrs['href']

			completeUrl = url + chapterUrl

			#print('%s:%s' % (title, completeUrl))

			d = {"title": title, "url": completeUrl}
			chapterArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"chapterArray": chapterArray}})

	except Exception as e:
		
		error = 'biquge_chapter_request：' + str(e)
		raise Exception(error)


def info_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:

			return soup

		info = soup.select('#info')[0]
		title = info.select('h1')[0].string
		#url = ""
		author = info.select('p')[0].string
		category = ""
		lastTime = info.select('p')[2].string
		newChapter = info.select('p')[3].select('a')[0].string
		newUrl = info.select('p')[3].select('a')[0].attrs['href']
		firstUrl = soup.select('#list dl dd a')[0].attrs['href']
		completFirstUrl = url + firstUrl

		intro = soup.select('#intro p')[0].string
		icon = soup.select('#fmimg img')[0].attrs['src']

		completeBookUrl = baseUrl + newUrl

		'''
		print(title)
		print(author)
		print(category)
		print('%s:%s %s' % (newChapter, completeBookUrl, lastTime))
		print(intro)
		print(icon)
		'''

		return json.dumps({"code": "6666", "des": "成功", "data": {"title": title, "url": url, "firstUrl": completFirstUrl, "author": author, "category": category, "newChapter": newChapter, "newUrl": completeBookUrl, "lastTime": lastTime, "intro": intro, "iconUrl": icon}})

	except Exception as e:
		
		error = 'biquge_info_request：' + str(e)
		raise Exception(error)


def content_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:

			return soup

		bookname = soup.select('.bookname')[0]
		bottem1 = soup.select('.bottem1 a')
		title = bookname.select('h1')[0].string
		previous = bottem1[0].attrs['href']
		bookUrl = bottem1[1].attrs['href']
		next = bottem1[2].attrs['href']
		content = soup.select('#content')[0].get_text()

		book = content.replace("    ", "\n    ")

		if book.startswith('\n'):

			book = book.lstrip('\n')

		completeBookUrl = baseUrl + bookUrl
		completePrevious = baseUrl + previous
		completeNext = baseUrl + next

		if completePrevious == completeBookUrl:

			completePrevious = ""

		if completeNext == completeBookUrl:

			completeNext = ""

		'''
		print(title)
		print(completeBookUrl)
		print(completePrevious)
		print(completeNext)
		print(book)
		'''

		return json.dumps({"code": "6666", "des": "成功", "data": {"title": title, "book": book, "previous": completePrevious, "next": completeNext}})

	except Exception as e:
		
		error = 'biquge_content_request：' + str(e)
		raise Exception(error)


if __name__ == '__main__':

	search_request('https://www.biduo.cc/search.php', {'keyword': '滚开'})
	#category_request('https://www.biduo.cc/book_1_1/')
	#info_request('https://www.biduo.cc/biquge/39_39809/')
	#chapter_request('https://www.biduo.cc/biquge/39_39809/')
	#content_request('https://www.biduo.cc/biquge/39_39809/c13239750.html')




