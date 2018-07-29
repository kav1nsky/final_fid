from django.contrib.auth import authenticate, login, logout

from reg.models import Profile
from .forms import RegForm, LoginForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from fidelity.fidelity import Fidelity

manager = Fidelity()

def reg_user(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            u = User.objects.create_user(username=form.cleaned_data['email'],
                                         password=form.cleaned_data['password'],)
            u.save()

            public_key, private_key, account_name = manager.createAccount(u.id)

            p = Profile(user=u, is_customer=False, real_name=form.cleaned_data['id_real_name'],
                        description=form.cleaned_data['bio'], public_key=public_key,
                        private_key=private_key, account_name=account_name)
            p.save()
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(request, user)
        return HttpResponseRedirect('profile')
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

@login_required
def profile(request):
    if request.method == 'GET':
        user_profile = Profile.objects.get(user=request.user.id)
        print(user_profile.public_key, "ewjifwefjoew")
        return HttpResponse(render(request, 'profile.html',
                                   {'user_profile' : user_profile}))