from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from vk_worker import upload_post_from_vk_group, show_all_groups, delete_row_group_from_user_library, update_post_from_vk_group
from env import credentials,project_id,private_key

@login_required
@csrf_exempt
def search_page(request):
	if request.method == 'GET':
		return render(request, 'vk_search.html', {'title': 'Поиск'})	
	elif request.method == 'POST':
		# pritn(request.POST)
		data = (upload_post_from_vk_group(request.user.username, request.POST.get('search'),project_id,credentials))
		print(data)
		return render(request, 'home.html')
	else:
		HttpResponseNotAllowed(['GET', 'POST'])

@login_required
@csrf_exempt
def user_posts(request):
	if request.method == 'GET':
		data = show_all_groups(request.user.username,project_id,credentials)
		print(data)
		return render(request, 'user_posts.html', {'data': data})
	elif request.method == 'POST':
		data = show_all_groups(request.user.username,project_id,credentials)
		if request.POST.get('author'):
			id = request.POST.get('author')
			print(data[int(id) - 1][0], data[int(id) - 1][1])
			data = delete_row_group_from_user_library(request.user.username, data[int(id) - 1][0],project_id=project_id,credentials=credentials)
		elif request.POST.get('update'):
			id = request.POST.get('update')
			print(data)
			print(id)
			update_post_from_vk_group(request.user.username, data[int(id) - 1][0],credentials=credentials)
		return render(request, 'user_posts.html', {'data': data})
	else:
		HttpResponseNotAllowed(['GET', 'POST'])

