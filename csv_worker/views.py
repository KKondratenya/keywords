from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from csv_worker.models import CSV
from csv_worker.forms import CsvForm
from django.conf import settings


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
		form = CsvForm(request.POST, request.FILES)
		print(request.FILES)
		if form.is_valid():
			new_csv = CSV(user=request.user, csv_file=form.cleaned_data['csv_file'])
			new_csv.save()
			new_form = CsvForm()
			return render(request, 'download_csv.html', {'form': new_form})
		form = CsvForm()
		return render(request, 'home.html', {'form': form})
			   
	else:
		HttpResponseNotAllowed(['GET', 'POST'])