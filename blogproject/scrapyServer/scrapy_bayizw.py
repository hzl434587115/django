#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#python scrapy_bayizw.py

from bs4 import BeautifulSoup
import requests
import json


baseUrl = "http://www.81zw.info"


def search_request(url, param):
	
	try:

		if len(url) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})
		elif len(param['keyword']) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})

		searchUrl = 'http://www.81zw.info/web/search.php'

		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		r = requests.get(url=searchUrl, headers=headers, params={'q': param['keyword']})
		soup = BeautifulSoup(r.text, features="html.parser")

		bookArray = list()

		total = '1'

		resultList = soup.select('#main .novelslist2 ul li')

		for result in resultList[1:]:

			info = result.select('span')
			title = info[1].select('a')[0].string
			url = info[1].select('a')[0].attrs['href']
			author = info[2].string
			category = info[0].string
			newChapter = info[3].select('a')[0].string
			newChapter = newChapter.replace("\n", "")
			newChapter = newChapter.replace(" ", "")
			newUrl = info[3].select('a')[0].attrs['href']
			intro = newChapter
			icon = ''
			lastTime = info[4].string

			completeUrl = baseUrl + url
			completeNewUrl = baseUrl + newUrl

			'''
			print('《%s》:%s' % (title, completeUrl))
			print('封面:%s' % icon)
			print('作者:%s' % author)
			print('%s:%s' % (newChapter, completeNewUrl))
			print('分类:%s' % category)
			print('更新时间:%s' % lastTime)
			print('简介:%s' % intro)
			'''

			d = {"title": title, "url": completeUrl, "newChapter": newChapter, "newUrl": completeNewUrl, "author": author, "lastTime": lastTime, "category": category, "intro": intro, "iconUrl": icon}
			bookArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"total": total, "bookArray": bookArray}})

	except requests.ConnectionError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except requests.HTTPError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except Exception as e:
		
		error = 'bayizw_search_request：' + str(e)
		raise Exception(error)


def base_request(url):

	try:
		
		if len(url) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})

		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
		r = requests.get(url=url, headers=headers).text
		soup = BeautifulSoup(r, features="html.parser")

		return soup

	except requests.ConnectionError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except requests.HTTPError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except Exception as e:
		
		error = 'bayizw_base_request：' + str(e)
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
		lastPage = soup.select('#PageBar ul li')[-3]
		total = lastPage.select('a')[0].string

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
			print('%s:%s' % (newChapter, baseUrl + newUrl))
			print('作者:%s' % author)
			'''

			d = {"title": title, "url": completeUrl, "newChapter": newChapter, "newUrl": completeNewUrl, "author": author, "intro": intro}
			bookArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"total": total, "bookArray": bookArray}})

	except Exception as e:
		
		error = 'bayizw_category_request：' + str(e)
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

			completeUrl = baseUrl + chapterUrl

			#print('%s:%s' % (title, completeUrl))

			d = {"title": title, "url": completeUrl}
			chapterArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"chapterArray": chapterArray}})

	except Exception as e:
		
		error = 'bayizw_chapter_request：' + str(e)
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
		completFirstUrl = baseUrl + firstUrl

		intro = soup.select('#intro')[0].string
		icon = soup.select('#fmimg img')[0].attrs['src']

		completeBookUrl = newUrl

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
		
		error = 'bayizw_info_request：' + str(e)
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

		completeBookUrl = bookUrl
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
		
		error = 'bayizw_content_request：' + str(e)
		raise Exception(error)


if __name__ == '__main__':

	search_request('http://www.81zw.info/web/search.php', {'keyword': '滚开'})
	#category_request('http://www.81zw.info/xuanhuanxiaoshuo/1.html')
	#info_request('http://www.81zw.info/book/3203/')
	#chapter_request('http://www.81zw.info/book/3203/')
	#content_request('http://www.81zw.info/book/3203/598481.html')




