from django.db import models
# 设置字段颜色
from django.utils.html import format_html, strip_tags
# f富文本
from DjangoUeditor.models import UEditorField
import html

class BlogUser(models.Model):

	account = models.CharField('账号', max_length=20, unique=True)
	password = models.CharField('密码', max_length=20)
	phone = models.CharField('手机号', max_length=20)
	name = models.CharField('昵称', max_length=20)
	userIcon = models.ImageField(upload_to='blog/images', default="blog/images/default_1.jpg")
	professional = models.CharField('职业', max_length=20, default="ios开发工程师")
	address = models.CharField('地址', max_length=20, default="上海市-闸北区")
	email = models.CharField('邮箱', max_length=20, default="602387134@qq.com")
	sign = models.CharField('签名', max_length=20, default="昆仑剑出血汪洋，千里直驱黄河黄")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = '博客用户表'


class Category(models.Model):

	name = models.CharField('分类', max_length=20)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = '分类表'

class Tag(models.Model):

	name = models.CharField('标签', max_length=20)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = '标签表'

class Status(models.Model):

	name = models.CharField('文章状态', max_length=10)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = '文章状态表'

class Post(models.Model):

	# 文章标题
	title = models.CharField('标题', max_length=100)
	# 文章正文
	#body = models.TextField('正文')
	body = UEditorField('正文', height=300, width=800, toolbars='full', blank=True, imagePath='blog/postImages/', filePath='blog/postFiles/')
	# 创建时间
	created_time = models.DateTimeField('创建时间' ,auto_now_add=True)
	# 修改时间
	modified_time = models.DateTimeField('修改时间' ,auto_now=True)
	# 文章状态
	status = models.ForeignKey(Status, verbose_name='文章状态', null=True, on_delete=models.SET_NULL)
	# 文章摘要
	excerpt = models.CharField('文章摘要', max_length=100, blank=True, null=True, help_text="可选，如若为空将摘取正文的前36个字符")
	# 浏览量
	views = models.PositiveIntegerField('浏览量', default=0)
	# 点赞量
	likes = models.PositiveIntegerField('点赞数', default=0)
	# 置顶
	topped = models.BooleanField('置顶', default=False)
	# 文章分类
	category = models.ForeignKey(Category, verbose_name='分类', null=True, on_delete=models.SET_NULL)
	# 文章标签
	tags = models.ManyToManyField(Tag, blank=True)
	# 文章作者
	author = models.ForeignKey(BlogUser, verbose_name='作者', null=True, on_delete=models.SET_NULL)

	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])

	def increase_likes(self):
		self.likes += 1
		self.save(update_fields=['likes'])

	# 重写父类save方法
	def save(self, *args, **kwargs):
		# 如果没有填写摘要
		if not self.excerpt:
			# 从文本摘取前 36 个字符赋给 excerpt
			str_body = strip_tags(self.body)
			# 处理html转译
			txt = html.unescape(str_body)
			self.excerpt = strip_tags(txt.lstrip())[:36]

		# 调用父类的 save 方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)

	# 设置字段颜色，在admin.py list_display=('colored_status')显示表格的表头
	def colored_status(self):

		if self.status.name == '发布':
			color_code = 'green'
		else:
			color_code = 'red'

		return format_html(
			'<span style="color: {};">{}</span>',
			color_code,
			self.status,
		)
	colored_status.short_description = u'文章状态'

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-created_time']
		verbose_name_plural = '文章表'

class Comment(models.Model):
	
	# 评论内容
	body = models.TextField('评论内容')
	# 创建时间
	created_time = models.DateTimeField('创建时间' ,auto_now_add=True)
	# 评论用户,related_name参数设置反向解析
	author = models.ForeignKey(BlogUser, verbose_name='评论用户', related_name="comments", null=True, on_delete=models.SET_NULL)
	# 评论所属文章
	post = models.ForeignKey(Post, verbose_name='评论所属文章', null=True, on_delete=models.SET_NULL)

	'''----------修改适应回复----------'''

	# 所属的根评论
	root = models.ForeignKey('self', verbose_name='顶级评论', related_name="root_comment", null=True, on_delete=models.SET_NULL)
	# 所属的评论或回复
	parent = models.ForeignKey('self', verbose_name='所属评论或回复', related_name="parent_comment", null=True, on_delete=models.SET_NULL)
	# 被回复的用户
	reply_to = models.ForeignKey(BlogUser, verbose_name='被回复用户', related_name="replies", null=True, on_delete=models.SET_NULL)

	def __str__(self):

		title = self.body

		if self.post is None:
			title = post.title

		return title + self.author.name

	class Meta:
		ordering = ['-created_time']
		verbose_name_plural = '评论表'
		
