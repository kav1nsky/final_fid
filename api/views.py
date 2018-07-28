from rest_framework import viewsets
from .serializers import *


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
   queryset = Profile.objects.all()

   def get_serializer_class(self):
       return ProfileSerializer