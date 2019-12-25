from django.contrib import admin
import os
from . import models

class ScrapyAdmin(admin.ModelAdmin):

	# 显示的列
	list_display = ['name', 'url', 'fileName']

	# 设置只读，在创建的时候 fileName 就是上传的文件名
	readonly_fields = ('fileName', )


	def save_model(self, request, obj, form, change):

		'''
		if change:

			obj_old = self.model.objects.get(pk=obj.pk)
			self.delete_file(obj.filePath.url)
		'''

		fileName = obj.filePath.url.replace("/media/", "")
		obj.fileName = fileName.replace(".py", "")

		super(ScrapyAdmin, self).save_model(request, obj, form, change)
		
	def delete_model(self, request, obj):

		# 删除爬虫模块相应的脚本文件，直接系统删除，手动删除才会在回收站
		self.delete_file(obj.filePath.url)
		super(ScrapyAdmin, self).delete_model(request, obj)

	def delete_file(self, path):
		
		fileName = path.replace("/media/", "")
		delete_file = 'scrapyServer/' + fileName
		os.remove(delete_file)


class CategoryAdmin(admin.ModelAdmin):

	# 显示的列
	list_display = ['name', 'url', 'scrapy']


admin.site.register(models.Scrapy, ScrapyAdmin)
admin.site.register(models.Category, CategoryAdmin)
