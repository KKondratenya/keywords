from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from search_articles import search, search_user_library
from similar_articles import create_description, find_similar, similar_articles_from_user_library

@login_required
@csrf_exempt
def search_page(request):
	if request.method == 'GET':
		return render(request, 'search.html', {'title': 'Поиск'})	
	elif request.method == 'POST':
		if not request.POST.get('choice'):
			choice = 'title'
		else:
			choice = request.POST.get('choice')
		search_data = request.POST.get('search')
		if request.POST.get('type_search') == 'users':
			data = (search_user_library(request.user.username, search_data, choice))
		else:
			data = (search(search_data, choice))
		print(data)
		return render(request, 'search_data.html', {'data': data[:10], 'search_data': search_data})
	else:
		HttpResponseNotAllowed(['GET', 'POST'])

@login_required
@csrf_exempt
def same_article(request):
	if request.method == 'GET':
		return render(request, 'article.html')	
	elif request.method == 'POST':
		if request.POST.get('create'):
			desciption = create_description(request.POST['article'], '', '')
			return render(request, 'article.html', {'article': desciption[0], 'keyword': desciption[1], 'annotation': desciption[2]})	
		elif request.POST.get('find_similiar'):
			if request.POST.get('type_search') == 'users':
				print(request.user.username)
				similar = similar_articles_from_user_library(request.user.username, request.POST['article'], request.POST['keyword'], request.POST['annotation'])
			else:
				similar = find_similar(request.POST['article'], request.POST['keyword'], request.POST['annotation'])
				print(similar)
			return render(request, 'article_with_data.html', {
				'article': request.POST['article'], 
				'keyword': request.POST['keyword'], 
				'annotation':request.POST['annotation'], 
				'data': similar})
		return render(request, 'article.html')
	else:
		HttpResponseNotAllowed(['GET', 'POST'])
	
