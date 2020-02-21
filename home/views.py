from django.shortcuts import render

from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserForm, RegistrForm
from home.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# Create your views here.
@login_required
def home(request):
	return render(request, 'home.html')

@csrf_exempt
def login1(request):
	if request.method == 'GET':
		form = UserForm()
		return render(request, 'login.html', {'form': form})	
	elif request.method == 'POST':
		# print(request.POST)
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			login(request, user)
			response = JsonResponse({'data':'data'})
			return render(request, 'home.html')
		return render(request, 'login.html', {'error': "Ошибка авторизации"})
	else:
		HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def registr(request):
	if request.method == 'GET':
		form = RegistrForm()
		return render(request, 'regis.html', {'form': form})	
	elif request.method == 'POST':
		form = RegistrForm(request.POST)
		if form.is_valid():
			print(form)
			user = User(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'])
			user.set_password(form.cleaned_data['password'])
			user.save()
			login(request, user)
		else:
			print(form.errors.as_data())
			return render(request, 'regis.html', {'form': form})
		return render(request, 'home.html')
	else:
		HttpResponseNotAllowed(['GET', 'POST'])