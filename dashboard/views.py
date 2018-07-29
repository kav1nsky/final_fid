from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView

from apps.dashboard.forms import AgreementForm
from apps.reg.models import Review, Profile, Agreement


# @login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'profile': profile[0]})


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

