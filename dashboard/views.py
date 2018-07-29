from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from dashboard.forms import AgreementForm
from reg.models import Review, Profile, Agreement


def profile_view(request, public_key):
    user_profile = Profile.objects.get(public_key=public_key)
    user_profile.private_key = None
    return render(request, 'profile.html', {'user_profile': user_profile})


@login_required
def create_agreement_view(request):
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            agreement = Agreement(customer=request.user,
                                  worker=User.objects.get(username=form.cleaned_data['email']),
                                  due=form.timestamp,
                                  state="initiated",
                                  content=form.cleaned_data['content'])
            agreement.save()

            return HttpResponse('Вы успешно разместили соглашение.')
    else:
        form = AgreementForm()

    return render(request, 'agreement.html', {'form': form})


def dashboard(request):
    if request.method == 'GET':
        return HttpResponse(render(request, 'dashboard.html'))