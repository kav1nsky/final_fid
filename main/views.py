from django.contrib.auth import authenticate, login

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def dashboard(request):
    pass