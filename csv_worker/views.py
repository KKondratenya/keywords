import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from csv_worker.models import CSV
from csv_worker.forms import CsvForm
from django.conf import settings
import csv
from csv_download import upload_user_bd


ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'csv'])

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@login_required
@csrf_exempt
def download(request):
	if request.method == 'GET':
		form = CsvForm()
		return render(request, 'download_csv.html', {'form': form})
	elif request.method == 'POST':
		arr = []
		if request.POST.get('save'):
			for i in request.POST:
				data = request.POST.getlist(i)
				if len(data) > 1:
					arr.append(data)
			upload_user_bd(arr, request.user.username)
		else:
			form = CsvForm(request.POST, request.FILES)
			# print(request.FILES)
			if form.is_valid():
				new_csv = CSV(user=request.user, csv_file=form.cleaned_data['csv_file'])
				new_csv.save()
				new_form = CsvForm()
				print()	
				path = settings.BASE_DIR + '/media/' + str(new_csv.csv_file)
				with open(path) as obj:
					reader = csv.reader(obj)
					data = list(reader)
					# for row in reader:
					# 	print(" ".join(row))
				new_csv.delete()
				os.remove(path)
				print(data)
				return render(request, 'edit_csv.html', {'csvs': data})
			form = CsvForm()
		return render(request, 'home.html')
			   
	else:
		HttpResponseNotAllowed(['GET', 'POST'])