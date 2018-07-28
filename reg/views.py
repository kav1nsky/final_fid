from django.contrib.auth import authenticate, login, logout

from reg.models import Profile
from .forms import RegForm, LoginForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from dj_project import eos

def reg_user(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(username=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'],)
            u.save()

            eos.create_new_account()

            p = Profile(user=u, is_customer=False, real_name=form.cleaned_data['bio'],
                        description=form.cleaned_data['bio'])
            p.save()
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
        return HttpResponseRedirect('/dashboard')
    else:
        form = RegForm()

    return HttpResponse(render(request, 'worker_reg.html', {'form': form}))


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['name'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
        return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return HttpResponse(render(request, 'login.html', {'form': form}))

@login_required
def exit(request):
    if request.method == 'GET':
        logout(request)
    return redirect('index')