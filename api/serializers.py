from rest_framework import serializers
from reg.models import Profile, Review, Agreement


class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
       model = Profile
       fields = [
           'user',
           'is_customer',
           'real_name',
           'rating',
           'description',
           'date_of_reg'
       ]