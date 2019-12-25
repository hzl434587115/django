import os
import xadmin
from . import models


class ScrapyAdmin(object):

	# 显示的列
	list_display = ['name', 'url', 'fileName']

	# 设置只读，在创建的时候 fileName 就是上传的文件名
	readonly_fields = ['fileName']

	'''
	def save_models(self):

		if self.org_obj is None:

			super(ScrapyAdmin, self).save_models()
		else:

			print('----------------不允许修改----------------')
			flag = 'change'
			self.log(flag, ['不允许修改'], self.new_obj)
	'''

	def save_models(self):

		super(ScrapyAdmin, self).save_models()

		if self.org_obj is None:

			# 在创建的时候 fileName 就是上传的文件名
			fileName = self.new_obj.filePath.url.replace("scrapyServer/", "")
			self.new_obj.fileName = fileName.replace(".py", "")
			self.new_obj.save()
		
	def delete_model(self):

		# 删除爬虫模块相应的脚本文件，直接系统删除，手动删除才会在回收站
		os.remove(self.obj.filePath.url)
		super(ScrapyAdmin, self).delete_model()


class CategoryAdmin(object):

	# 显示的列
	list_display = ['name', 'url', 'scrapy']


xadmin.site.register(models.Scrapy, ScrapyAdmin)
xadmin.site.register(models.Category, CategoryAdmin)
