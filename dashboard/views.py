from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import CreateView
from apps.reg.models import Review

@login_required
def my_profile_view(request):
    request



class CreateReview(CreateView):
    model = Review
    # queryset =
    fields = [
        'customer', 'worker', 'content', 'timestamp'
    ]


