from django.contrib import admin
from django.contrib.auth.models import User
from .models import BlogUser, Category, Tag, Status, Post, Comment

# 用户名：hzl
# 密码：hzl666666

class BloUserAdmin(admin.ModelAdmin):

	readonly_fields = ('account', )

	list_display = ['account', 'name', 'phone']
	fields =  (('account', ), ('password', ), ('name', ), ('phone', ), ('userIcon', ))

	def get_queryset(self,request):
		
		userList = super(BloUserAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return userList
		return userList.filter(account=request.user.username)

	def save_model(self, request, obj, form, change):

		if change:

			first_name = ''
			last_name = ''
			if len(obj.name) > 1:
				last_name = obj.name[:1]
			if len(obj.name) >= 2:
				first_name = obj.name[1:len(obj.name)]

			print(obj.name)
			print(last_name)
			print(first_name)

			user = User.objects.get(username=obj.account)

			user.username = obj.account
			user.first_name = first_name
			user.last_name = last_name
			user.set_password(obj.password)
			user.save()
		else:

			first_name = ''
			last_name = ''
			if len(obj.name) > 1:
				first_name = obj.name[:1]
			elif len(obj.name) > 2:
				last_name = obj.name[1:len(obj)]

			user = User.objects.create_user(username=obj.account, password=obj.password, first_name=first_name, last_name=last_name)
			user.save()

		super(BloUserAdmin, self).save_model(request, obj, form, change)
		

class PostAdmin(admin.ModelAdmin):
	#listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
	list_display = ['title', 'colored_status', 'created_time', 'category', 'author']
	#list_per_page设置每页显示多少条记录，默认是100条
	list_per_page = 10
	#ordering设置默认排序字段，负号表示降序排序
	ordering = ('created_time',)
	#搜索字段
	search_fields = ('title', 'body')
	#筛选器，过滤器
	list_filter = ('category', 'author')
	# 详细时间分层筛选
	date_hierarchy = 'created_time'
	filter_horizontal = ('tags',)
	#list_editable 设置默认可编辑字段
	#list_editable = ['author']

	readonly_fields = ('author', )

	def get_queryset(self,request):
		
		postList = super(PostAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return postList
		author = BlogUser.objects.get(account=request.user.username)
		return postList.filter(author=author)

class CommentAdmin(admin.ModelAdmin):
	#listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
	list_display = ['author', 'created_time']
	#list_per_page设置每页显示多少条记录，默认是100条
	list_per_page = 10
	#ordering设置默认排序字段，负号表示降序排序
	ordering = ('created_time',)
	#搜索字段
	search_fields = ('author', 'body')
	#筛选器，过滤器
	list_filter = ('author',)
	# 详细时间分层筛选
	date_hierarchy = 'created_time'

	readonly_fields = ('author', 'post', )

	def get_queryset(self,request):
		
		commentList = super(CommentAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return commentList
		author = BlogUser.objects.get(account=request.user.username)
		return commentList.filter(author=author)

class CategoryAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj=None):
		"""  重新定义此函数，限制普通用户所能修改的字段  """
		if request.user.is_superuser:
			self.readonly_fields = []
		return self.readonly_fields

	readonly_fields = ('name', )

class TagAdmin(admin.ModelAdmin):

	def get_readonly_fields(self, request, obj=None):
		"""  重新定义此函数，限制普通用户所能修改的字段  """
		if request.user.is_superuser:
			self.readonly_fields = []

		return self.readonly_fields

	readonly_fields = ('name', )

admin.site.site_header = '昆仑' # 设置标题
admin.site.site_title = '昆仑' # 设置标题

admin.site.register(BlogUser, BloUserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Status)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
