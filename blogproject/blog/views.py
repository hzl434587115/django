from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import BlogUser, Category, Tag, Status, Post, Comment


# 首页
def index(request):

	topList = Post.objects.filter(topped=True)[:6]
	newList = Post.objects.order_by('-created_time')[:6]
	readList = Post.objects.order_by('-views')[:6]
	#dateList = Post.objects.dates('created_time', 'month', order='DESC') #归档文章日期
	context = {'topList': topList, 'newList': newList, 'readList': readList}
	context.update(userData(request))

	return render(request, 'blog/index.html', context)

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

	return render(request, 'blog/bloglist.html', context)

# 根据作者查询文章
def blogdetails(request, blog_id):

	post = Post.objects.get(pk=blog_id)
	# 阅读量 +1
	post.increase_views()

	categoryList = Category.objects.all()
	readList = Post.objects.order_by('-views')[:6]
	topList = Post.objects.filter(topped=True)[:6]
	commentList = Comment.objects.filter(post=blog_id)
	context = {'post': post, 'categoryList': categoryList, 'readList': readList, 'topList': topList, 'commentList': commentList}
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

	return render(request, 'blog/about.html', context)

def loginView(request):
	
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

	return index(request)

def comment(request):

	try:

		userID = request.session['userID']
		author = BlogUser.objects.get(pk=userID)
		body = request.POST.get('content')
		post_id = request.POST.get('post_id')
		post = Post.objects.get(pk=post_id)

		comment = Comment.objects.create(body=body, author=author, post=post)
		post.increase_likes()
		return HttpResponse(u'评论成功')

	except KeyError:
		return HttpResponse(u'评论失败')
	else:
		return HttpResponse(u'评论失败')

# 测试可选参数方法
def test(request, year):
	
	print(year)
	return HttpResponse(u"昆仑")

def userData(request):

	try:

		state = request.session['state']
		userID = request.session['userID']
		name = request.session['name']
		account = request.session['account']
		return {'state': state, 'name': name, 'account': account, 'userID': userID}

	except KeyError:
		return {}

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

	if len(left) < number:

		for x in range(0, number - len(left)):
			pageNum = right[-1] + 1
			if pageNum >= 1:
				right.append(pageNum)

	elif len(right) < number:

		for x in range(0, number - len(right)):
			pageNum = left[0] - 1
			if pageNum <= totalPage:
				left.insert(0, pageNum)

	beforePage = page - 1
	afterPage = page + 1

	return {'left': left, 'page': page, 'right': right, 'totalPage': totalPage, 'beforePage': beforePage, 'afterPage': afterPage}
