from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_customer = models.BooleanField()
    real_name = models.CharField(max_length=200)
    rating = models.IntegerField(default=-1)
    description = models.TextField()
    date_of_reg = models.DateTimeField(default=datetime.now())


class Review(models.Model):
    customer = models.ForeignKey(User, related_name='customer_rev', on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name='worker_rev', on_delete=models.CASCADE)
    content = models.TextField()
    mark = models.IntegerField()
    timestamp = models.DateTimeField()


class Agreement(models.Model):
    customer = models.ForeignKey(User, related_name='customer_agr', on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name='worker_agr',on_delete=models.CASCADE)
    state = models.CharField(max_length=20)
    content = models.TextField()
    due = models.DateTimeField()





