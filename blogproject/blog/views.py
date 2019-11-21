from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import BlogUser, Category, Tag, Status, Post, Comment

# 首页
def index(request):

	try:
		
		topList = Post.objects.filter(topped=True)[:6]
		newList = Post.objects.order_by('-created_time')[:6]
		readList = Post.objects.order_by('-views')[:6]
		#dateList = Post.objects.dates('created_time', 'month', order='DESC') #归档文章日期
		context = {'topList': topList, 'newList': newList, 'readList': readList}
		context.update(userData(request))
		context.update(userInfo(request))

		return render(request, 'blog/index.html', context)
	except Exception as e:
		print(e)
		

# 所有文章
def blogList(request, page):

	# 返回数据数
	maxResult = 2
	# 切片的索引
	start = (page - 1)* maxResult
	end = start + maxResult
	totalRecord = Post.objects.count()

	pageDict = pageData(totalRecord, page)

	categoryList = Category.objects.all()
	postList = Post.objects.all()[start:end]
	readList = Post.objects.order_by('-views')[:6]
	topList = Post.objects.filter(topped=True)[:6]
	context = {'categoryList': categoryList, 'postList': postList, 'readList': readList, 'topList': topList}
	context.update(pageDict)
	context.update(userData(request))

	return render(request, 'blog/bloglist.html', context)

# 所有文章
def categoryList(request, category_id, page):

	# 返回数据数
	maxResult = 2
	# 切片的索引
	start = (page - 1) * maxResult
	end = start + maxResult

	totalRecord = Post.objects.filter(category_id=category_id).count()

	pageDict = pageData(totalRecord, page)

	categoryList = Category.objects.all()
	postList = Post.objects.filter(category_id=category_id)[start:end]
	readList = Post.objects.order_by('-views')[:6]
	topList = Post.objects.filter(topped=True)[:6]
	context = {'categoryList': categoryList, 'postList': postList, 'readList': readList, 'topList': topList, 'category_id': category_id}
	context.update(pageDict)
	context.update(userData(request))

	return render(request, 'blog/categoryList.html', context)

# 根据作者查询文章
def blogdetails(request, blog_id):

	post = Post.objects.get(pk=blog_id)
	# 阅读量 +1
	post.increase_views()

	pre_blog = Post.objects.filter(pk__gt=blog_id).order_by('pk')    # 上一篇
	next_blog = Post.objects.filter(pk__lt=blog_id).order_by('-pk')  # 下一篇

		#取第1条记录
	if pre_blog.count() > 0:
		pre_blog = pre_blog[0]
	else:
		pre_blog = None
	    
	if next_blog.count() > 0:
		next_blog = next_blog[0]
	else:
		next_blog = None

	categoryList = Category.objects.all()
	readList = Post.objects.order_by('-views')[:6]
	topList = Post.objects.filter(topped=True)[:6]
	commentList = Comment.objects.filter(post=blog_id,parent=None).order_by('-created_time')
	context = {'post': post, 'pre_blog': pre_blog, 'next_blog': next_blog, 'categoryList': categoryList, 'readList': readList, 'topList': topList, 'commentList': commentList}
	context.update(userData(request))
	return render(request, 'blog/blogdetails.html', context)

# 根据作者查询文章
def share(request):

	userList = BlogUser.objects.all()
	categoryList = Category.objects.all()
	readList = Post.objects.order_by('-views')[:6]
	topList = Post.objects.filter(topped=True)[:6]
	groupList = [userList, userList, userList]
	context = {'groupList': groupList, 'categoryList': categoryList, 'readList': readList, 'topList': topList}
	context.update(userData(request))
	return render(request, 'blog/share.html', context)

# 根据作者查询文章
def user(request, user_id):

	postList = Post.objects.filter(author=user_id)
	context = {'postList': postList}
	return render(request, 'blog/postList.html', context)

# 关于我
def about(request):

	categoryList = Category.objects.all()
	context = {'categoryList': categoryList}
	context.update(userData(request))
	context.update(userInfo(request))

	return render(request, 'blog/about.html', context)

def loginView(request):
	
	#print(request.GET.get('next'))
	#print(request.GET.get('a'))

	return render(request, 'blog/login.html')

def login(request):

	try:

		account = request.POST.get('account')
		password = request.POST.get('password')

		user = BlogUser.objects.get(account=account)

		if user.password == password:

			request.session['state'] = '1'
			request.session['userID'] = user.pk
			request.session['name'] = user.name
			request.session['account'] = user.account

			return HttpResponse(u'登录成功')
		else:
			return HttpResponse(u'密码错误')

	except BlogUser.DoesNotExist:
		return HttpResponse(u'用户不存在')
	else:
		return HttpResponse(u'系统错误')

def logout(request):

	del request.session['state']
	del request.session['userID']
	del request.session['name']
	del request.session['account']

	#return index(request)
	return HttpResponseRedirect(reverse('blog:index'))

def comment(request):

	try:

		userID = request.session['userID']
		author = BlogUser.objects.get(pk=userID)
		body = request.POST.get('content')
		post_id = request.POST.get('post_id')
		post = Post.objects.get(pk=post_id)

		replyTo_id = request.POST.get('replyTo_id')

		if len(replyTo_id) > 0:

			root_id = request.POST.get('root_id')
			parent_id = request.POST.get('parent_id')
			reply_to = BlogUser.objects.get(pk=replyTo_id)
			root = Comment.objects.get(pk=root_id)
			parent = Comment.objects.get(pk=parent_id)
			comment = Comment.objects.create(body=body, author=author, post=post, root=root, parent=parent, reply_to=reply_to)

		else:
			comment = Comment.objects.create(body=body, author=author, post=post)
		post.increase_likes()
		return HttpResponse(u'评论成功')

	except KeyError:
		return HttpResponse(u'评论失败')
	else:
		return HttpResponse(u'评论失败')


def userData(request):

	try:

		state = request.session['state']
		userID = request.session['userID']
		name = request.session['name']
		account = request.session['account']
		return {'state': state, 'name': name, 'account': account, 'userID': userID}

	except KeyError:
		return {}

def userInfo(request):
	
	try:

		account = request.session['account']

		if account is None:

			userIcon = '/media/blog/images/icon_default.jpg'

			return {'account': '', 'userIcon': userIcon, 'sign': '', 'name': '', 'professional': '', 'address': '', 'phone': '', 'email': ''}

		user = BlogUser.objects.get(account=account)

		userIcon = user.userIcon.url

		return {'account': account, 'userIcon': user.userIcon.url, 'sign': user.sign,'name': user.name, 'professional': user.professional, 'address': user.address, 'phone': user.phone, 'email': user.email}

	except KeyError:

		userIcon = '/media/blog/images/icon_default.jpg'

		return {'account': '', 'userIcon': userIcon, 'sign': '', 'name': '', 'professional': '', 'address': '', 'phone': '', 'email': ''}

# 分页
def pageData(totalRecord, page):
	
	# 当前page两边各3位，123(4)567
	number = 3
	# 返回数据数
	maxResult = 2
	# 总页数
	totalPage = (totalRecord + maxResult - 1) // maxResult
	# 当前页左边连续的页码号，初始值为空
	left = []
	# 当前页右边连续的页码号，初始值为空
	right = []
	# 计算应显示的页数
	pageNum = page

	for x in range(1, number + 1):
		
		pageNum = page - x
		if pageNum >= 1:
			left.insert(0, pageNum)

	for x in range(1, number + 1):

		pageNum = page + x
		if pageNum <= totalPage:
			right.append(pageNum)

	#print(right)

	if len(left) < number:

		for x in range(0, number - len(left)):

			if len(right) > 0:

				pageNum = right[-1] + 1
				if pageNum >= 1 and pageNum <= totalPage:
					right.append(pageNum)

	elif len(right) < number:

		for x in range(0, number - len(right)):

			if len(left) > 0:

				pageNum = left[0] - 1
				if pageNum >= 1 and pageNum <= totalPage:
					left.insert(0, pageNum)

	#print(right)

	beforePage = page - 1
	afterPage = page + 1

	return {'left': left, 'page': page, 'right': right, 'totalPage': totalPage, 'beforePage': beforePage, 'afterPage': afterPage}
