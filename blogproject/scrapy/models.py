from django.db import models
from django.core.files.storage import FileSystemStorage

# 指定上传文件目录无论 MEDIA_ROOT设置是什么
fs = FileSystemStorage(location='scrapyServer')


class Scrapy(models.Model):
	
	name = models.CharField('名称', max_length=50, default='')
	url = models.CharField('网址', max_length=100, default='')
	fileName = models.CharField('模块', max_length=100, default='')
	#filePath = models.FileField('文件', upload_to='scrapyServer/', max_length=100)
	filePath = models.FileField('文件', storage=fs, max_length=100)
	# 创建时间
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	# 修改时间
	modified_time = models.DateTimeField('修改时间', auto_now=True)

	class Meta:
		verbose_name = '网站'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


class Category(models.Model):
	
	name = models.CharField('名称', max_length=50, default='')
	url = models.CharField('网址', max_length=100, default='')
	# 页码需要替换的文本
	pageReplace = models.CharField('页码', max_length=20, default='')
	scrapy = models.ForeignKey(Scrapy, verbose_name='网站', null=True, on_delete=models.SET_NULL)
	# 创建时间
	created_time = models.DateTimeField('创建时间', auto_now_add=True)
	# 修改时间
	modified_time = models.DateTimeField('修改时间', auto_now=True)

	class Meta:
		verbose_name = '网文分类'
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
