from django.contrib import admin


from django.contrib import admin
from .models import Profile, Review, Agreement

for i in [Profile, Review, Agreement]:
    admin.site.register(i)