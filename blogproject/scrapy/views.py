from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import importlib

from . import models


def base_request(request, functionName, param):
	
	try:

		fileName = ''
		url = ''

		if request.method == 'POST':

			fileName = request.POST.get('fileName', None)
			url = request.POST.get('url', None)

			if len(fileName) == 0 or len(url) == 0:
				return json.dumps({"code": "1001", "des": "参数错误"})
		else:

			return json.dumps({"code": "1002", "des": "请用post方法请求"})

		moduleName = 'scrapyServer.' + fileName
		module = importlib.import_module(moduleName)
		function = getattr(module, functionName)

		if len(param) == 0:

			return function(url)

		return function(url, param)

	except Exception as e:

		print('----------------------异常开始----------------------')
		print(str(e))
		print('----------------------异常结束----------------------')
		return json.dumps({"code": "1003", "des": '系统异常'})


@csrf_exempt
def search_request(request):

	response = base_request(request, 'search_request', {'keyword': request.POST.get('keyword', '')})

	return HttpResponse(response)


@csrf_exempt
def category_request(request):

	response = base_request(request, 'category_request', {})

	return HttpResponse(response)


@csrf_exempt
def chapter_request(request):

	response = base_request(request, 'chapter_request', {})

	return HttpResponse(response)


@csrf_exempt
def info_request(request):

	response = base_request(request, 'info_request', {})

	return HttpResponse(response)


@csrf_exempt
def content_request(request):

	response = base_request(request, 'content_request', {})

	return HttpResponse(response)


@csrf_exempt
def source_request(request):

	try:

		if request.method == 'POST':

			scrapyList = models.Scrapy.objects.all()
			sourceList = list()

			for scrapy in scrapyList:

				categoryList = list(models.Category.objects.filter(scrapy=scrapy).values("name", "url", "pageReplace"))
				sourceList.append({"name": scrapy.name, "fileName": scrapy.fileName, "categoryList": categoryList})

			return HttpResponse(json.dumps({"code": "6666", "des": "成功", "data": {"sourceList": sourceList}}))
		else:

			return HttpResponse(json.dumps({"code": "1002", "des": "请用post方法请求"}))

	except Exception as e:

		print('----------------------异常开始----------------------')
		print('view_source_request：' + str(e))
		print('----------------------异常结束----------------------')
		return json.dumps({"code": "1003", "des": "系统异常"})


@csrf_exempt
def test_request(request):

	fileName = ''
	url = ''

	if request.method == 'POST':

		fileName = request.POST.get('fileName', None)
		url = request.POST.get('url', None)
	else:

		return HttpResponse(json.dumps({"code": "1002", "des": "请用post方法请求"}))

	if len(fileName) == 0 or len(url) == 0:
		return HttpResponse(json.dumps({"code": "1001", "des": "参数错误"}))

	moduleName = 'scrapyServer.' + fileName

	return HttpResponse(json.dumps({"code": "6666", "des": "成功", "data": moduleName}))

