#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#python scrapy_dingdian.py

from bs4 import BeautifulSoup
import requests
import json


baseUrl = "https://www.ddxs.cc"


def search_request(url, param):

	if len(param['keyword']) == 0:

		return json.dumps({"code": "1001", "des": "参数错误"})

	return json.dumps({"code": "1004", "des": "功能未开通"})


def base_request(url):

	try:
		
		if len(url) == 0:

			return json.dumps({"code": "1001", "des": "参数错误"})

		headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
		r = requests.get(url=url, headers=headers)
		soup = BeautifulSoup(r.text, features="html.parser")

		return soup

	except requests.ConnectionError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except requests.HTTPError as e:

		return json.dumps({"code": "1003", "des": "网络连接错误"})
	except Exception as e:
		
		error = 'dingdian_base_request：' + str(e)
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
		total = soup.select('#newscontent .l .page_b #pagelink .last')[0].string

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
		
		error = 'dingdian_category_request：' + str(e)
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
			url = chapter.attrs['href']

			completeUrl = baseUrl + url

			#print('%s:%s' % (title, completeUrl))

			d = {"title": title, "url": completeUrl}
			chapterArray.append(d)

		return json.dumps({"code": "6666", "des": "成功", "data": {"chapterArray": chapterArray}})

	except Exception as e:
		
		error = 'dingdian_chapter_request：' + str(e)
		raise Exception(error)


def info_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:

			return soup

		info = soup.select('#info')[0]
		title = info.select('h1')[0].string
		url = ""
		author = info.select('p')[0].string
		category = info.select('p')[1].string
		newChapter = info.select('p')[2].select('strong a')[0].string
		newUrl = info.select('p')[2].select('strong a')[0].attrs['href']
		lastTime = info.select('p')[3].select('strong time')[0].string
		firstUrl = soup.select('#list dl dd a')[0].attrs['href']
		completFirstUrl = baseUrl + firstUrl

		intro = soup.select('#intro p')[0].string
		icon = soup.select('#fmimg img')[0].attrs['src']

		'''
		print(title)
		print(author)
		print(category)
		print('%s:%s %s' % (newChapter, newUrl, lastTime))
		print(intro)
		print(icon)
		'''

		return json.dumps({"code": "6666", "des": "成功", "data": {"title": title, "url": url, "firstUrl": completFirstUrl, "author": author, "category": category, "newChapter": newChapter, "newUrl": newUrl, "lastTime": lastTime, "intro": intro, "iconUrl": icon}})

	except Exception as e:
		
		error = 'dingdian_info_request：' + str(e)
		raise Exception(error)


def content_request(url):
	
	try:

		soup = base_request(url)

		if isinstance(soup, BeautifulSoup) == False:

			return soup

		bookname = soup.select('.bookname')[0]
		bottem1 = soup.select('.bottem1 a')
		title = bookname.select('h1')[0].string
		previous = bottem1[1].attrs['href']
		bookUrl = bottem1[2].attrs['href']
		next = bottem1[3].attrs['href']
		content = soup.select('#content')[0].get_text()

		book = content.replace("    ", "\n    ")

		if book.startswith('\n'):

			book = book.lstrip('\n')

		completePrevious = baseUrl + previous
		completeNext = baseUrl + next

		if completePrevious == bookUrl:

			completePrevious = ""

		if completeNext == bookUrl:

			completeNext = ""

		'''
		print(title)
		print(completePrevious)
		print(completeNext)
		print(book)
		'''

		return json.dumps({"code": "6666", "des": "成功", "data": {"title": title, "book": book, "previous": completePrevious, "next": completeNext}})

	except Exception as e:
		
		error = 'dingdian_content_request：' + str(e)
		raise Exception(error)


if __name__ == '__main__':

	#category_request('https://www.ddxs.cc/xuanhuanxiaoshuo/1_1.html')
	#info_request('https://www.ddxs.cc/ddxs/773/')
	#chapter_request('https://www.ddxs.cc/ddxs/773/')
	content_request('https://www.ddxs.cc/ddxs/773/13979933.html')




