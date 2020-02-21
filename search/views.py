from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from search_articles import search

@login_required
@csrf_exempt
def search_page(request):
	if request.method == 'GET':
		return render(request, 'search.html')	
	elif request.method == 'POST':
		if request.POST.get('choice'):
			choice = 'title'
		else:
			choice = request.POST.get('choice')
		search_data = request.POST.get('search')
		data = (search(search_data, choice))
		return render(request, 'search_data.html', {'data': data})
	else:
		HttpResponseNotAllowed(['GET', 'POST'])